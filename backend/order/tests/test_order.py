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

def get_user_order_by_order_id(id):
    return reverse('order:user-order', args=(id,))

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
        self.user_token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}



    def test_create_order_success(self):
        """Test creating a new order."""

        res = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user']['id'], self.user.id)
        self.assertEqual(res.data['shippingAddress']['address'], self.order['shippingAddress']['address'])


    def test_create_order_unsuccess(self):
        """Test unsuccess creating a new order."""
        del self.order['orderItems']

        res = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_order_unsuccess_unauthorized(self):
        """Test unsuccess creating a new order with an unauthorized user."""

        res = self.client.post(CREATE_ORDER_URL, self.order, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_order_authorized_user_success(self):
        """Test success getting order related to the user."""

        res1 = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res2 = self.client.get(get_user_order_by_order_id(res1.data['id']), **self.user_token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, res1.data)


    def test_get_user_order_by_admin_success(self):
        """Test success getting user's order with admin authorization."""

        admin_params = {
            'first_name': 'Test Admin',
            'email': 'admin@mail.com',
            'username': 'admin@mail.com',
            'password': 'password123',
        }

        create_user(admin_params, True)
        token_res = get_token(self.client.post, admin_params)
        admin_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        res1 = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res2 = self.client.get(get_user_order_by_order_id(res1.data['id']), **admin_token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, res1.data)


    def test_get_order_authorized_user_unsuccess(self):
        """Test getting order not exists by the user."""

        res1 = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res2 = self.client.get(get_user_order_by_order_id(res1.data['id']+1), **self.user_token)

        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_user_order_by_other_user_unsuccess(self):
        """Test getting user's order with diffrent user."""

        other_user_params = {
            'first_name': 'Test Other',
            'email': 'other@mail.com',
            'username': 'other@mail.com',
            'password': 'password123',
        }

        create_user(other_user_params)
        token_res = get_token(self.client.post, other_user_params)
        other_user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        res1 = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res2 = self.client.get(get_user_order_by_order_id(res1.data['id']), **other_user_token)

        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)


