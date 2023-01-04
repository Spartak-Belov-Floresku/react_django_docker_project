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
GET_USER_ORDERS = reverse('order:myorders')

def deliver_orde_url(id):
    return reverse('order:order-delivered', args=(id,))

def get_user_order_by_order_id(id):
    return reverse('order:user-order', args=(id,))

def pay_order_url(id):
    return reverse('order:pay', args=(id,))

def create_user(params):
    """Create and return a new user."""
    return User.objects.create_user(**params)

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


    def test_get_user_orders_success(self):
        """Test getting user orders."""

        self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')

        res_user_orders = self.client.get(GET_USER_ORDERS, **self.user_token)

        self.assertEqual(res_user_orders.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_user_orders.data), 2)


    def test_get_unauthenticated_user_orders_ussuccess(self):
        """Test getting unauthenticated user orders ussuccess."""

        self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')

        res_user_orders = self.client.get(GET_USER_ORDERS)

        self.assertEqual(res_user_orders.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_order_authorized_user_success(self):
        """Test success getting order related to the user."""

        res1 = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res2 = self.client.get(get_user_order_by_order_id(res1.data['id']), **self.user_token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, res1.data)


    def test_get_order_authorized_user_unsuccess(self):
        """Test getting order not exists by the user."""

        res_user_order = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res_user_not_order = self.client.get(get_user_order_by_order_id(res_user_order.data['id']+1), **self.user_token)

        self.assertEqual(res_user_not_order.status_code, status.HTTP_400_BAD_REQUEST)


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

        res_user = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res_other_user = self.client.get(get_user_order_by_order_id(res_user.data['id']), **other_user_token)

        self.assertEqual(res_other_user.status_code, status.HTTP_400_BAD_REQUEST)


    def test_pay_order_success(self):
        """Test to pay order by authenticated user."""

        res_create_order = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res_pay_order = self.client.put(pay_order_url(res_create_order.data['id']), **self.user_token)
        res_confirmed_order_was_paied = self.client.get(get_user_order_by_order_id(res_create_order.data['id']), **self.user_token)

        self.assertEqual(res_pay_order.status_code, status.HTTP_200_OK)
        self.assertEqual(res_confirmed_order_was_paied.data['isPaid'], True)


    def test_pay_order_unauthenticated_user_unsuccess(self):
        """Test to pay order by unauthenticated user."""

        res_create_order = self.client.post(CREATE_ORDER_URL, self.order, **self.user_token, format='json')
        res_pay_order = self.client.put(pay_order_url(res_create_order.data['id']))

        self.assertEqual(res_pay_order.status_code, status.HTTP_401_UNAUTHORIZED)
