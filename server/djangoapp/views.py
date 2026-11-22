import json
import logging
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from .models import CarModel
from .restapis import analyze_review_sentiments, get_request, post_review

logger = logging.getLogger(__name__)


def _body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON") from exc


def _error(message, status=400):
    return JsonResponse({"status": status, "error": message}, status=status)


@ensure_csrf_cookie
@require_GET
def csrf_token(request):
    return JsonResponse({"status": 200})


@require_POST
def login_user(request):
    try:
        data = _body(request)
        user = authenticate(username=data.get("userName", ""), password=data.get("password", ""))
        if user is None:
            return _error("Invalid username or password", 401)
        login(request, user)
        return JsonResponse({"status": "Authenticated", "userName": user.username,
                             "firstName": user.first_name, "lastName": user.last_name})
    except ValueError as exc:
        return _error(str(exc))


@require_POST
def logout_request(request):
    logout(request)
    return JsonResponse({"status": 200})


@require_POST
def registration(request):
    try:
        data = _body(request)
        username, password = data.get("userName", "").strip(), data.get("password", "")
        if not username or len(password) < 8:
            return _error("Username and an 8-character password are required")
        if User.objects.filter(username=username).exists():
            return _error("Username already exists", 409)
        user = User.objects.create_user(username=username, password=password,
            first_name=data.get("firstName", "").strip(), last_name=data.get("lastName", "").strip(),
            email=data.get("email", "").strip())
        login(request, user)
        return JsonResponse({"status": 200, "userName": user.username,
            "firstName": user.first_name, "lastName": user.last_name})
    except ValueError as exc:
        return _error(str(exc))


@require_GET
def get_dealerships(request, state=None):
    try:
        endpoint = "fetchDealers" if not state else f"fetchDealers/{state}"
        return JsonResponse({"status": 200, "dealers": get_request(endpoint)})
    except requests.RequestException:
        logger.exception("Dealership API unavailable")
        return _error("Dealership service unavailable", 503)


@require_GET
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = get_request(f"fetchReviews/dealer/{dealer_id}")
        for review in reviews:
            review["sentiment"] = analyze_review_sentiments(review.get("review", ""))
        return JsonResponse({"status": 200, "reviews": reviews})
    except requests.RequestException:
        logger.exception("Review service unavailable")
        return _error("Review service unavailable", 503)


@require_GET
def get_dealer_details(request, dealer_id):
    try:
        return JsonResponse({"status": 200, "dealer": get_request(f"fetchDealer/{dealer_id}")})
    except requests.RequestException:
        logger.exception("Dealership API unavailable")
        return _error("Dealership service unavailable", 503)


@require_GET
def get_cars(request):
    cars = [{"CarMake": car.car_make.name, "CarModel": car.name, "CarYear": car.year}
            for car in CarModel.objects.select_related("car_make").order_by("car_make__name", "name")]
    return JsonResponse({"status": 200, "CarModels": cars})


@require_POST
def add_review(request):
    if not request.user.is_authenticated:
        return _error("Authentication required", 401)
    try:
        data = _body(request)
        data["name"] = request.user.get_full_name() or request.user.username
        return JsonResponse({"status": 200, "review": post_review(data)})
    except (ValueError, requests.RequestException):
        logger.exception("Unable to submit review")
        return _error("Unable to submit review", 502)


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})
