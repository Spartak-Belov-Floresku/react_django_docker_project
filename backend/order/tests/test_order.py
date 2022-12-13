"""
Tests for the order API.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import *

TOKEN_URL = reverse('user:user-token')
CREATE_ORDER_URL = reverse('order:orders-add')

def create_user(params, admin=False):
    """Create and return a new user."""
    if not admin:
        return User.objects.create_user(**params)
    else:
        return User.objects.create_superuser(**params)

def get_token(path, params):
    """Create and return a token."""
    return path(TOKEN_URL, params)


class OrderAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'Test Name',
            'email': 'test@mail.com',
            'username': 'test@mail.com',
            'password': 'password123',
        }
        self.user = create_user(self.payload)
        res = get_token(self.client.post, self.payload)
        self.token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}



    def test_create_order_success(self):
        """Test creating a new user."""
        payload = {
            'name': 'Name',
            'email': 'test2@mail.com',
            'password': 'password123',
        }
        res = self.client.post(CREATE_ORDER_URL, payload, **self.token, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)