import json
from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import CarMake, CarModel, ContactMessage, Dealership, Review


class CarwiseApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dealer = Dealership.objects.create(
            id=9999, city="Lusaka", state="Lusaka", st="LS",
            address="1 Great North Road", zip="10101", lat=-15.4,
            long=28.3, short_name="Carwise", full_name="Carwise Motors",
        )
        make, _ = CarMake.objects.get_or_create(name="Toyota")
        CarModel.objects.create(car_make=make, name="RAV4", type="SUV", year=2025)

    def post_json(self, path, payload):
        return self.client.post(path, json.dumps(payload), content_type="application/json")

    def test_health(self):
        self.assertEqual(self.client.get("/djangoapp/health").json()["status"], 200)

    def test_register_session_logout_and_login(self):
        payload = {"firstName":"Ada","lastName":"Driver","userName":"ada",
                   "email":"ada@example.com","password":"SafePass123!"}
        response = self.post_json("/djangoapp/register", payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.client.get("/djangoapp/session").json()["authenticated"])
        self.assertEqual(self.client.get("/djangoapp/logout").status_code, 200)
        self.assertFalse(self.client.get("/djangoapp/session").json()["authenticated"])
        response = self.post_json("/djangoapp/login", {"userName":"ada","password":"SafePass123!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")

    def test_registration_rejects_duplicates_and_short_passwords(self):
        short = {"firstName":"A","lastName":"B","userName":"ab",
                 "email":"ab@example.com","password":"short"}
        self.assertEqual(self.post_json("/djangoapp/register", short).status_code, 400)
        User.objects.create_user("taken", email="taken@example.com", password="SafePass123!")
        duplicate = {**short, "userName":"taken", "email":"new@example.com", "password":"SafePass123!"}
        self.assertEqual(self.post_json("/djangoapp/register", duplicate).status_code, 409)

    def test_invalid_login_is_rejected(self):
        response = self.post_json("/djangoapp/login", {"userName":"missing","password":"wrong"})
        self.assertEqual(response.status_code, 401)

    def test_dealer_list_filter_and_detail(self):
        self.assertGreaterEqual(len(self.client.get("/djangoapp/get_dealers").json()["dealers"]), 1)
        self.assertEqual(len(self.client.get("/djangoapp/get_dealers/Lusaka").json()["dealers"]), 1)
        self.assertEqual(len(self.client.get("/djangoapp/get_dealers/Atlantis").json()["dealers"]), 0)
        self.assertEqual(self.client.get("/djangoapp/dealer/9999").json()["dealer"][0]["full_name"], "Carwise Motors")
        self.assertEqual(self.client.get("/djangoapp/dealer/999").status_code, 404)

    def test_car_models_are_available(self):
        cars = self.client.get("/djangoapp/get_cars").json()["CarModels"]
        rav4 = next(car for car in cars if car["CarModel"] == "RAV4")
        self.assertEqual(rav4["CarMake"], "Toyota")

    def test_review_requires_login_then_creates_with_sentiment(self):
        payload = {"name":"Ada Driver","dealership":9999,"review":"Great friendly service",
                   "purchase":True,"purchase_date":"2026-11-05","car_make":"Toyota",
                   "car_model":"RAV4","car_year":2025}
        self.assertEqual(self.post_json("/djangoapp/add_review", payload).status_code, 401)
        User.objects.create_user("ada", password="SafePass123!")
        self.client.login(username="ada", password="SafePass123!")
        response = self.post_json("/djangoapp/add_review", payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["review"]["sentiment"], "positive")
        reviews = self.client.get("/djangoapp/reviews/dealer/9999").json()["reviews"]
        self.assertEqual(reviews[0]["review"], "Great friendly service")
        self.assertEqual(
            Review.objects.get(dealership=self.dealer).purchase_date,
            date(2026, 11, 5),
        )

    def test_contact_message_is_stored(self):
        response = self.post_json("/djangoapp/contact", {
            "first_name":"Ada", "last_name":"Driver",
            "email":"ada@example.com", "message":"Please contact me.",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.count(), 1)

