from django.urls import reverse
from django.test import TestCase
from rest_framework import status

# Create your tests here.
class RegisterationTest(TestCase):
    " Test case for registering a new athlete "

    def setUp(self):
        self.valid_payload = {
            'email': 'test3@example.com',
            'password': 'test123'
        }
        self.invalid_payload = {
            'email': '',
            'password': 'test123'
        }

    def test_create_valid_athlete(self):
        response = self.client.post(
            reverse('registration'),
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_athlete(self):
        response = self.client.post(
            reverse('registration'),
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)