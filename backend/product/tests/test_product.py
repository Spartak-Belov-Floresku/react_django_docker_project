"""
Tests for the product API.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer


ALL_PRODUCTS_URL = reverse('product:products')

def product_detail_url(id):
    """Return a product detail url."""
    return reverse('product:product', args=(id,))

def create_user():
    """Create and return a new user."""
    defaults = {
        'first_name': 'testname',
        'username': 'test@mail.com',
        'email': 'test@mail.com',
        'password': 'password123',
    }

    return User.objects.create_superuser(**defaults)

def create_product(user):
    """Create and return a product"""
    product = Product.objects.create(
        user=user,
        name='Sample product name',
        description='Sample product description',
        price=Decimal('5.50'),
        active=True,
    )

    return product


class ProductAPITests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.product = create_product(self.user)

    def test_retrive_products_success(self):
        """Test retrieving a list of products."""
        res_products = self.client.get(ALL_PRODUCTS_URL)
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res_products.status_code, status.HTTP_200_OK)
        self.assertEqual(res_products.data, serializer.data)


    def test_get_product_success(self):
        """Testing the reciving of a specific product."""
        res_product_details = self.client.get(product_detail_url(self.product.id))
        serializer = ProductSerializer(self.product, many=False)

        self.assertEqual(res_product_details.status_code, status.HTTP_200_OK)
        self.assertEqual(res_product_details.data, serializer.data)


    def test_get_product_unsuccess(self):
        """Testing the reciving a product that doesn't exist."""
        res_product_details = self.client.get(product_detail_url(100))

        self.assertEqual(res_product_details.status_code, status.HTTP_400_BAD_REQUEST)