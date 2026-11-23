import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarModel, ContactMessage, Dealership, Review


def _payload(request):
    try:
        return json.loads(request.body or "{}")
    except (TypeError, json.JSONDecodeError):
        return None


def _error(message, status=400):
    return JsonResponse({"status": status, "message": message}, status=status)


def _sentiment(text):
    words = set(text.lower().replace(".", " ").replace(",", " ").split())
    positive = {"amazing", "excellent", "friendly", "good", "great", "helpful",
                "honest", "love", "professional", "recommend", "smooth", "trusted"}
    negative = {"awful", "bad", "dishonest", "poor", "rude", "slow", "terrible",
                "unhelpful", "worst"}
    score = len(words & positive) - len(words & negative)
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


@require_http_methods(["GET"])
def health(request):
    return JsonResponse({"status": 200, "service": "carwise"})


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    data = _payload(request)
    if data is None:
        return _error("Invalid JSON.")
    username = (data.get("userName") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip()
    first_name = (data.get("firstName") or "").strip()
    last_name = (data.get("lastName") or "").strip()
    if not all((username, password, email, first_name, last_name)):
        return _error("All registration fields are required.")
    if len(password) < 8:
        return _error("Password must contain at least 8 characters.")
    if User.objects.filter(username__iexact=username).exists():
        return _error("That username is already in use.", 409)
    if User.objects.filter(email__iexact=email).exists():
        return _error("That email address is already registered.", 409)
    user = User.objects.create_user(
        username=username, password=password, email=email,
        first_name=first_name, last_name=last_name,
    )
    login(request, user)
    return JsonResponse({
        "status": "Authenticated", "userName": user.username,
        "firstName": user.first_name, "lastName": user.last_name,
    }, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    data = _payload(request)
    if data is None:
        return _error("Invalid JSON.")
    username = (data.get("userName") or "").strip()
    user = authenticate(request, username=username, password=data.get("password") or "")
    if user is None:
        return _error("The username or password is incorrect.", 401)
    login(request, user)
    return JsonResponse({
        "status": "Authenticated", "userName": user.username,
        "firstName": user.first_name, "lastName": user.last_name,
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({"status": 200, "message": "Logged out."})


@require_http_methods(["GET"])
def session_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse({
        "authenticated": True, "userName": request.user.username,
        "firstName": request.user.first_name, "lastName": request.user.last_name,
    })


@require_http_methods(["GET"])
def get_dealerships(request, state=None):
    dealers = Dealership.objects.all()
    if state and state.lower() != "all":
        dealers = dealers.filter(state__iexact=state)
    return JsonResponse({"status": 200, "dealers": [d.as_dict() for d in dealers]})


@require_http_methods(["GET"])
def get_dealer_details(request, dealer_id):
    dealer = Dealership.objects.filter(pk=dealer_id).first()
    if dealer is None:
        return _error("Dealership not found.", 404)
    return JsonResponse({"status": 200, "dealer": [dealer.as_dict()]})


@require_http_methods(["GET"])
def get_dealer_reviews(request, dealer_id):
    if not Dealership.objects.filter(pk=dealer_id).exists():
        return _error("Dealership not found.", 404)
    reviews = Review.objects.filter(dealership_id=dealer_id)
    return JsonResponse({"status": 200, "reviews": [r.as_dict() for r in reviews]})


@require_http_methods(["GET"])
def get_cars(request):
    cars = CarModel.objects.select_related("car_make").all()
    return JsonResponse({"status": 200, "CarModels": [{
        "id": car.id, "CarMake": car.car_make.name,
        "CarModel": car.name, "CarType": car.type, "CarYear": car.year,
    } for car in cars]})


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    if not request.user.is_authenticated:
        return _error("Authentication is required to post a review.", 401)
    data = _payload(request)
    if data is None:
        return _error("Invalid JSON.")
    required = ("dealership", "review", "purchase_date", "car_make", "car_model", "car_year")
    if any(data.get(key) in (None, "") for key in required):
        return _error("All review fields are required.")
    dealer = Dealership.objects.filter(pk=data["dealership"]).first()
    if dealer is None:
        return _error("Dealership not found.", 404)
    try:
        purchase_date = datetime.strptime(data["purchase_date"], "%Y-%m-%d").date()
        car_year = int(data["car_year"])
    except (TypeError, ValueError):
        return _error("Purchase date or vehicle year is invalid.")
    review = Review.objects.create(
        name=(data.get("name") or request.user.get_full_name() or request.user.username).strip(),
        dealership=dealer, review=data["review"].strip(),
        purchase=bool(data.get("purchase", True)), purchase_date=purchase_date,
        car_make=data["car_make"].strip(), car_model=data["car_model"].strip(),
        car_year=car_year, sentiment=_sentiment(data["review"]),
    )
    return JsonResponse({"status": 200, "review": review.as_dict()}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def contact(request):
    data = _payload(request)
    if data is None:
        return _error("Invalid JSON.")
    values = {key: (data.get(key) or "").strip()
              for key in ("first_name", "last_name", "email", "message")}
    if not all(values.values()):
        return _error("All contact fields are required.")
    item = ContactMessage.objects.create(**values)
    return JsonResponse({"status": 200, "id": item.id,
                         "message": "Thanks — your message has been received."}, status=201)
