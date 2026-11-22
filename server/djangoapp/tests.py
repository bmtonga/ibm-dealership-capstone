import json
from django.test import Client, TestCase, override_settings
from .models import CarMake, CarModel


@override_settings(SECURE_SSL_REDIRECT=False, CSRF_COOKIE_SECURE=False, SESSION_COOKIE_SECURE=False)
class ApplicationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def csrf(self):
        response = self.client.get('/djangoapp/csrf')
        self.assertEqual(response.status_code, 200)
        return response.cookies['csrftoken'].value

    def test_registration_login_and_logout(self):
        token = self.csrf()
        response = self.client.post('/djangoapp/register',
            data=json.dumps({'userName': 'demo', 'password': 'StrongPass123!'}),
            content_type='application/json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        token = self.client.cookies['csrftoken'].value
        response = self.client.post('/djangoapp/logout', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)

    def test_csrf_is_required(self):
        response = self.client.post('/djangoapp/register', data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_cars_endpoint(self):
        make = CarMake.objects.create(name='Test Make')
        CarModel.objects.create(car_make=make, name='Test Model', type='SUV', year=2025)
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Make', [car['CarMake'] for car in response.json()['CarModels']])
