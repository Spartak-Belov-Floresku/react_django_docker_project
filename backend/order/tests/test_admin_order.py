"""
Tests for the orderadmin API.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import *

TOKEN_URL = reverse('user:user-token')
GET_ORDERS = reverse('order:orders')
CREATE_ORDER_URL = reverse('order:orders-add')
GET_USER_ORDERS = reverse('order:myorders')

def deliver_orde_url(id):
    return reverse('order:order-delivered', args=(id,))

def get_user_order_by_order_id(id):
    return reverse('order:user-order', args=(id,))

def pay_order_url(id):
    return reverse('order:pay', args=(id,))

def create_admin(params, admin=False):
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
    """Test authenticated admin API requests."""

    def setUp(self):
        self.client = APIClient()
        self.admin_payload = {
            'first_name': 'Admin User',
            'email': 'admin@mail.com',
            'username': 'admin@mail.com',
            'password': 'password123',
        }
        self.admin = create_admin(self.admin_payload, True)
        self.product = create_product(self.admin)
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
        res = get_token(self.client.post, self.admin_payload)
        self.admin_token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}


    def test_get_user_order_by_admin_success(self):
        """Test success getting user's order with admin authorization."""

        user_params = {
            'first_name': 'Test User',
            'email': 'user@mail.com',
            'username': 'user@mail.com',
            'password': 'password123',
        }

        create_admin(user_params)
        token_res = get_token(self.client.post, user_params)
        user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        res_user = self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        res_admin = self.client.get(get_user_order_by_order_id(res_user.data['id']), **self.admin_token)

        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(res_admin.data, res_user.data)


    def test_mark_order_as_delivered_by_admin_success(self):
        """Test set order as delivered with admin authorization."""

        user_params = {
            'first_name': 'Test User',
            'email': 'user@mail.com',
            'username': 'user@mail.com',
            'password': 'password123',
        }

        create_admin(user_params)
        token_res = get_token(self.client.post, user_params)
        user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        res_create_order = self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        res_mark_order_delivered = self.client.put(deliver_orde_url(res_create_order.data['id']), **self.admin_token)
        res_get_order_by_user = self.client.get(get_user_order_by_order_id(res_create_order.data['id']), **user_token)

        self.assertEqual(res_mark_order_delivered.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get_order_by_user.data['isDelivered'], True)


    def test_mark_order_as_delivered_by_user_unsuccess(self):
        """Test set order as delivered with user authorization unsuccess."""
        user_params = {
            'first_name': 'Test User',
            'email': 'user@mail.com',
            'username': 'user@mail.com',
            'password': 'password123',
        }

        create_admin(user_params)
        token_res = get_token(self.client.post, user_params)
        user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        res_create_order = self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        res_mark_order_delivered = self.client.put(deliver_orde_url(res_create_order.data['id']), **user_token)

        self.assertEqual(res_mark_order_delivered.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_orders_as_admin_success(self):
        """Test get orders using admin authorization."""

        user_params = {
            'first_name': 'Test User',
            'email': 'user@mail.com',
            'username': 'user@mail.com',
            'password': 'password123',
        }

        create_admin(user_params)
        token_res = get_token(self.client.post, user_params)
        user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        res_all_orders = self.client.get(GET_ORDERS, **self.admin_token)

        self.assertEqual(res_all_orders.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_all_orders.data), 2)


    def test_get_orders_as_user_unsuccess(self):
        """Test get orders without admin privileges."""

        user_params = {
            'first_name': 'Test User',
            'email': 'user@mail.com',
            'username': 'user@mail.com',
            'password': 'password123',
        }

        create_admin(user_params)
        token_res = get_token(self.client.post, user_params)
        user_token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}

        self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        self.client.post(CREATE_ORDER_URL, self.order, **user_token, format='json')
        res_all_orders = self.client.get(GET_ORDERS, **user_token)

        self.assertEqual(res_all_orders.status_code, status.HTTP_403_FORBIDDEN)
