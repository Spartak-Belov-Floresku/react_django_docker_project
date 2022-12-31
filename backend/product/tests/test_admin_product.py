"""
Tests for the product admin API.
"""
from decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer

TOKEN_URL = reverse('user:user-token')
GET_ALL_PRODUCTS = reverse('product:admin-products')
CREATE_PRODUCT_URL = reverse('product:create-product')

def update_product_url(id):
    """Update product url."""
    return reverse('product:update-product', args=(id,))

def product_delete_url(id):
    """Delete product url."""
    return reverse('product:delete-product', args=(id,))

def create_admin(params):
    """Create and return a new user."""
    defaults = {
        'first_name': 'testname',
        'username': 'test@mail.com',
        'email': 'test@mail.com',
        'password': 'password123',
    }
    defaults.update(params)
    return User.objects.create_superuser(**defaults)

def get_token(path, params):
    """Create and return a token."""
    token = path(TOKEN_URL, params)
    return {'HTTP_AUTHORIZATION': f'Bearer {token.data.get("token")}'}

def create_product(user, active=False):
    """Create and return a product"""
    product = Product.objects.create(
        user=user,
        name='Sample product name',
        image='product.jpg',
        description='Sample product description',
        price=Decimal('5.50'),
        active=active,
    )

    return product


class AdminProductAPITests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()
        self.admin_data = {
            'first_name': 'Admin Name',
            'username': 'admin@mail.com',
            'email': 'admin@mail.com',
            'password': 'password123',
        }
        self.admin = create_admin(self.admin_data)
        self.token = get_token(self.client.post, self.admin_data)
        self.product = create_product(self.admin)

    def test_get_products_by_admin_success(self):
        """Test get all products using admin authentication."""
        res_product = self.client.get(GET_ALL_PRODUCTS, **self.token)

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_product.data), 1)

    def test_get_products_by_admin_unsuccess(self):
        """Test get all products without admin authentication."""
        res_product = self.client.get(GET_ALL_PRODUCTS)

        self.assertEqual(res_product.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_success(self):
        """Test creates product."""
        res_product = self.client.post(CREATE_PRODUCT_URL, **self.token)
        product_exists = Product.objects.filter(id=res_product.data['id']).exists()

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertTrue(product_exists)

    def test_create_product_unsuccess(self):
        """Test creates product without valid token."""
        res_product = self.client.post(CREATE_PRODUCT_URL)

        self.assertEqual(res_product.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product_success(self):
        """Test updates product."""
        product_serializer = ProductSerializer(self.product, many=False)
        updated_payload = product_serializer.data

        updated_payload['name'] = 'Updated Name'
        updated_payload['active'] = True

        res_product = self.client.put(update_product_url(self.product.id), updated_payload, **self.token, format='json')
        product_update = Product.objects.get(id=self.product.id)
        product_serializer = ProductSerializer(product_update, many=False)

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertEqual(res_product.data, product_serializer.data)

    def test_update_product_unsuccess(self):
        """Test updates product without valid token."""
        product_serializer = ProductSerializer(self.product, many=False)
        updated_payload = product_serializer.data

        updated_payload['name'] = 'Updated Name'

        res_product = self.client.put(update_product_url(self.product.id), updated_payload, format='json')

        self.assertEqual(res_product.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_product_success(self):
        """Test deletes product."""
        res_product_deleted = self.client.delete(product_delete_url(self.product.id), **self.token)
        product_exists = Product.objects.filter(id=self.product.id).exists()

        self.assertEqual(res_product_deleted.status_code, status.HTTP_200_OK)
        self.assertFalse(product_exists)


    def test_delete_product_unsuccess(self):
        """Test ubsuccessful deletes product."""
        res_product_deleted = self.client.delete(product_delete_url(self.product.id))

        self.assertEqual(res_product_deleted.status_code, status.HTTP_401_UNAUTHORIZED)