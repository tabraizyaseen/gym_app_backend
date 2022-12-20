import json
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import Equipments

# Create your tests here.
class ExcerciseTest(TestCase):
    " Test case for recording an excercise and generating reports"

    def setUp(self):
        self.valid_payload = {
            "duration" : 150,
            "description": "Running on threadmill for 5 mints",
            "calories_burnt": 20,
            "equipment": "treadmills"
        }
        self.invalid_payload = {
            "description": "Running on threadmill for 5 mints",
            "calories_burnt": 20,
            "equipment": "treadmills"
        }
        self.user = get_user_model().objects.create_user(password='12test12', email='test@example.com')
        self.equipment = Equipments.objects.create(name='treadmills')
        self.user.save()
        self.equipment.save()
        token , _ = Token.objects.get_or_create(user_id=self.user.id)
        self.token_key = token.key

    def tearDown(self):
        self.user.delete()
        self.equipment.delete()

    def test_record_excercise(self):
        response = self.client.post(
            reverse('do_excercise'),
            data=self.valid_payload,
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_record_excercise(self):
        response = self.client.post(
            reverse('do_excercise'),
            data=self.invalid_payload,
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_excercise_report(self):
        print((datetime.now() - timedelta(days=1)).isoformat())
        response = self.client.get(
            reverse('excercises_report'),
            data={
                "start": (datetime.now() - timedelta(days=1)).isoformat(),
                "end": (datetime.now()).isoformat()
            },
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_excercise_report(self):
        response = self.client.get(
            reverse('excercises_report'),
            data={'end': datetime.now()},
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthentication_athlete(self):
        response = self.client.post(
            reverse('do_excercise'),
            data=self.invalid_payload,
            HTTP_AUTHORIZATION=f"Token invalid_token",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EquipmentTest(TestCase):
    " Test case for registering a new equipment "

    def setUp(self):
        self.valid_payload = {"name": "treadmills"}
        self.invalid_payload = {"name": ""}
        self.user = get_user_model().objects.create_user(password='12test12', email='test@example.com')
        self.user.save()
        token , _ = Token.objects.get_or_create(user_id=self.user.id)
        self.token_key = token.key

    def tearDown(self):
        self.user.delete()

    def test_register_equipment(self):
        print(self.valid_payload)
        response = self.client.post(
            reverse('register_equipment'),
            data=self.valid_payload,
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_register_equipment(self):
        response = self.client.post(
            reverse('register_equipment'),
            data=self.invalid_payload,
            HTTP_AUTHORIZATION=f"Token {self.token_key}",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



