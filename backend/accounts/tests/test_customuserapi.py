from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


CREATE_USER_URL = reverse('accounts:create')


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # password is not returned in the response
        self.assertNotIn('password', res.data)
        token = Token.objects.get(user__email=payload['email'])
        self.assertEqual(token.key, res.data['token'])
