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

def create_product(user):
    """Create and return a product"""
    product = Product.objects.create(
        user=user,
        name='Sample product name',
        description='Sample product description',
        price=Decimal('5.50')
    )

    return product

def get_token(path, params):
    """Create and return a token."""
    return path(TOKEN_URL, params)


class OrderAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user_payload = {
            'first_name': 'Test Name',
            'email': 'test@mail.com',
            'username': 'test@mail.com',
            'password': 'password123',
        }
        self.user = create_user(self.user_payload)
        self.product = create_product(self.user)
        self.order = {
            'orderItems': [
                {
                    'product': self.product.id,
                    'price': self.product.price,
                    'qty': 1
                }
            ],
            'shippingAddress': {
                    'address': 'Ocean Street',
                    'city': 'Key West, FL',
                    'zipCode': '00001'
                },
            'paymentMethod': 'PayPal',
            'itemsPrice': self.product.price,
            'shippingPrice': '10.00',
            'totalPrice': self.product.price+10
        }
        res = get_token(self.client.post, self.user_payload)
        self.token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}



    def test_create_order_success(self):
        """Test creating a new order."""

        res = self.client.post(CREATE_ORDER_URL, self.order, **self.token, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user']['id'], self.user.id)
        self.assertEqual(res.data['shippingAddress']['address'], self.order['shippingAddress']['address'])


    def test_create_order_unsuccess(self):
        """Test unsuccess creating a new order."""
        del self.order['orderItems']

        res = self.client.post(CREATE_ORDER_URL, self.order, **self.token, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_order_unsuccess_unauthorized(self):
        """Test unsuccess creating a new order with an unauthorized user."""

        res = self.client.post(CREATE_ORDER_URL, self.order, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)