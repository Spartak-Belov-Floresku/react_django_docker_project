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


def product_detail_url(id):
    """Return a product detail url."""
    return reverse('product:product', args=(id,))

def get_token(path, params):
    """Create and return a token."""
    token = path(reverse('user:user-token'), params)
    return {'HTTP_AUTHORIZATION': f'Bearer {token.data.get("token")}'}

def create_review(id):
    """Retern review result."""
    return reverse('product:create-review', args=(id,))

def create_user(data):
    """Create and return a new user."""
    return User.objects.create_superuser(**data)

def create_product(user, params=False):
    """Create and return a product"""
    defaults = {
        'user': user,
        'name': 'Sample product name',
        'description':'Sample product description',
        'price': Decimal('5.50'),
        'active': True,
    }
    if params:
        defaults.update(params)
    product = Product.objects.create(**defaults)

    return product


class ProductAPITests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()
        self.defaults = {
            'first_name': 'testname',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'password123',
        }
        self.user = create_user(self.defaults)
        self.product = create_product(user=self.user)
        self.token = get_token(self.client.post, self.defaults)

    def test_retrive_products_success(self):
        """Test retrieving a list of products."""
        res_products = self.client.get('/api/products/')
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res_products.status_code, status.HTTP_200_OK)
        self.assertEqual(res_products.data['products'], serializer.data)


    def test_search_products_success(self):
        """Test search for products matching the name."""
        create_product(user=self.user, params={'name': 'yxz'})
        res_products_by_serch = self.client.get('/api/products/', {'keyword':'y'})

        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res_products_by_serch.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res_products_by_serch.data, serializer.data)


    def test_get_product_success(self):
        """Testing the reciving of a specific product."""
        res_product_details = self.client.get(f'/api/products/{self.product.id}/')
        serializer = ProductSerializer(self.product, many=False)

        self.assertEqual(res_product_details.status_code, status.HTTP_200_OK)
        self.assertEqual(res_product_details.data, serializer.data)


    def test_get_product_unsuccess(self):
        """Testing the reciving a product that doesn't exist."""
        res_product_details = self.client.get('/api/products/100/')

        self.assertEqual(res_product_details.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_reveiw_success(self):
    #     """Test create user reveiw for a product."""
    #     reveiw = {'rating': 5}
    #     res_product_reveiw = self.client.post(create_review(self.product.id), reveiw, **self.token, format='json')
    #     product = Product.objects.get(id=self.product.id)
    #     serializer = ProductSerializer(product, many=False)

    #     self.assertEqual(res_product_reveiw.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Decimal(reveiw['rating']), Decimal(serializer.data['rating']))

    # def test_create_reveiw_unsuccess(self):
    #     """Test create the second review to the same product."""
    #     reveiw = {'rating': 5}
    #     self.client.post(create_review(self.product.id), reveiw, **self.token, format='json')
    #     res_product_reveiw = self.client.post(create_review(self.product.id), reveiw, **self.token, format='json')

    #     self.assertEqual(res_product_reveiw.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual('Product already reviewed!', res_product_reveiw.data['detail'])

    # def test_create_reveiw_no_rating_unsuccess(self):
    #     """Test create review no rating."""
    #     res_product_reveiw = self.client.post(create_review(self.product.id), {'comment':'No rating'}, **self.token, format='json')

    #     self.assertEqual(res_product_reveiw.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual('Please select rating!', res_product_reveiw.data['detail'])

    # def test_create_reveiw_no_user_unsuccess(self):
    #     """Test create review without authentication."""
    #     reveiw = {'rating': 5}
    #     res_product_reveiw = self.client.post(create_review(self.product.id), reveiw, format='json')

    #     self.assertEqual(res_product_reveiw.status_code, status.HTTP_401_UNAUTHORIZED)
