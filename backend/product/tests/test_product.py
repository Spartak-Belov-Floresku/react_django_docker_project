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

def create_user(admin=False, **params):
    """Create and return a new user."""
    defaults = {
        'first_name': 'testname',
        'username': 'test@mail.com',
        'email': 'test@mail.com',
        'password': 'password123',
    }
    defaults.update(params)

    if not admin:
        return User.objects.create_user(**defaults)
    else:
        return User.objects.create_superuser(**defaults)

def create_product(user):
    """Create and return a product"""
    product = Product.objects.create(
        user=user,
        name='Sample product name',
        description='Sample product description',
        price=Decimal('5.50')
    )

    return product


class ProductAPITests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.product = create_product(self.user)

    def test_retrive_products(self):
        """Test retrieving a list of products."""
        res = self.client.get(ALL_PRODUCTS_URL)
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_get_product(self):
        """Testing the reciving of a specific product."""
        res = self.client.get(product_detail_url(self.product.id))
        serializer = ProductSerializer(self.product, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_get_product_unsuccess(self):
        """Testing the reciving a product that doesn't exist."""
        res = self.client.get(product_detail_url(100))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)