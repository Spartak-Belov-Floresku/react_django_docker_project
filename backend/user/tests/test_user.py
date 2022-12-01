"""
Tests for the user API.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import UserSerializerWithToken

TOKEN_URL = reverse('user:user-token')
PROFILE_URL = reverse('user:user-profile')

def create_user(**params):
    """Create and return a new user."""
    return User.objects.create_user(**params)


class UserAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'Test Name',
            'email': ' test@mail.com',
            'username': 'test@mail.com',
            'password': 'password123',
        }
        self.user = create_user(**self.payload)
        # self.client.force_authenticate(self.user)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""

        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""

        payload = {
            'email': 'none@mail.com',
            'password': 'testpassword',
            }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unathorized(self):
        """Test authentication is required for user."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_profile_success(self):
        """Test retrieving profile for valid token in user."""

        res1 = self.client.post(TOKEN_URL, self.payload)
        token = f'Bearer {res1.data.get("token")}'

        res2 = self.client.get(PROFILE_URL, **{'HTTP_AUTHORIZATION': token})

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'name': self.user.first_name,
            'isAdmin': False
        })