"""
Tests for the product admin API.
"""
from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from core.models import Product

from product.serializers import ProductSerializer

TOKEN_URL = reverse('user:user-token')

def update_product_url(id):
    """Update product url."""
    return reverse('product:update-product', args=(id,))

def product_delete_url(id):
    """Delete product url."""
    return reverse('product:delete-product', args=(id,))

def create_admin():
    """Create and return a new admin user."""
    defaults = {
        'first_name': 'testname',
        'username': 'admin@mail.com',
        'email': 'admin@mail.com',
        'password': 'password123',
    }
    return User.objects.create_superuser(**defaults), defaults

def create_user():
    """Create and return a new user."""
    defaults = {
        'first_name': 'testname',
        'username': 'user@mail.com',
        'email': 'user@mail.com',
        'password': 'password123',
    }
    return User.objects.create_user(**defaults), defaults

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
        self.admin, self.payload_admin = create_admin()
        self.user, self.payload_user = create_user()
        self.token_admin = get_token(self.client.post, self.payload_admin)
        self.token_user = get_token(self.client.post, self.payload_user)
        self.product = create_product(self.admin)

    def test_get_products_by_admin_success(self):
        """Test get all products using admin authentication."""
        res_product = self.client.get('/api/products/admin/list/products/', **self.token_admin)

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_product.data), 1)

    def test_get_products_by_admin_unsuccess(self):
        """Test get all products without admin authentication."""
        res_product = self.client.get('/api/products/admin/list/products/', **self.token_user)

        self.assertEqual(res_product.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unactive_products_by_admin_success(self):
        """Test get unactive products using admin authentication."""
        create_product(self.admin, True)
        create_product(self.admin, True)
        create_product(self.admin, True)
        create_product(self.admin, False)
        res_product = self.client.get('/api/products/admin/list/products/', {'unactive': True}, **self.token_admin)

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_product.data), 2)

    def test_create_product_success(self):
        """Test creates product."""
        res_product = self.client.post('/api/products/admin/create/product/', **self.token_admin)
        product_exists = Product.objects.filter(id=res_product.data['id']).exists()

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertTrue(product_exists)

    def test_create_product_unsuccess(self):
        """Test creates product without valid token."""
        res_product = self.client.post('/api/products/admin/create/product/', **self.token_user)

        self.assertEqual(res_product.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_success(self):
        """Test updates product."""
        product_serializer = ProductSerializer(self.product, many=False)
        updated_payload = product_serializer.data

        updated_payload['name'] = 'Updated Name'
        updated_payload['active'] = True

        res_product = self.client.put(f'/api/products/admin/update/product/{self.product.id}/', updated_payload, **self.token_admin, format='json')
        product_update = Product.objects.get(id=self.product.id)
        product_serializer = ProductSerializer(product_update, many=False)

        self.assertEqual(res_product.status_code, status.HTTP_200_OK)
        self.assertEqual(product_serializer.data['name'], updated_payload['name'])
        self.assertEqual(product_serializer.data['active'], updated_payload['active'])

    def test_update_product_unsuccess(self):
        """Test updates product without valid token."""
        product_serializer = ProductSerializer(self.product, many=False)
        updated_payload = product_serializer.data

        updated_payload['name'] = 'Updated Name'

        res_product = self.client.put(f'/api/products/admin/update/product/{self.product.id}/', updated_payload, **self.token_user, format='json')

        self.assertEqual(res_product.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_product_success(self):
        """Test deletes product."""
        res_product_deleted = self.client.delete(f'/api/products/admin/delete/product/{self.product.id}/', **self.token_admin)
        product_exists = Product.objects.filter(id=self.product.id).exists()

        self.assertEqual(res_product_deleted.status_code, status.HTTP_200_OK)
        self.assertFalse(product_exists)


    def test_delete_product_unsuccess(self):
        """Test ubsuccessful deletes product."""
        res_product_deleted = self.client.delete(f'/api/products/admin/delete/product/{self.product.id}/', **self.token_user)

        self.assertEqual(res_product_deleted.status_code, status.HTTP_403_FORBIDDEN)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.admin, self.payload_admin = create_admin()
        self.user, self.payload_user = create_user()
        self.token_admin = get_token(self.client.post, self.payload_admin)
        self.token_user = get_token(self.client.post, self.payload_user)
        self.product = create_product(self.admin)

    def tearDown(self):
        self.product.image.delete()


    def test_upload_image(self):
        """Test uploading image to a product."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file, 'product_id': self.product.id}
            res = self.client.post('/api/products/admin/image/product/', payload, **self.token_admin, fromat='multipart')

        self.product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('Image was uploaded', res.data)
        self.assertTrue(os.path.exists(self.product.image.path))

    def test_update_image(self):
        """Test updating image to a product."""

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file, 'product_id': self.product.id}
            res = self.client.post('/api/products/admin/image/product/', payload, **self.token_admin, fromat='multipart')

        self.product.refresh_from_db()
        old_path = self.product.image.path

        with tempfile.NamedTemporaryFile(suffix='.jpg') as new_image_file:
            new_img = Image.new('RGB', (10, 10))
            new_img.save(new_image_file, format='JPEG')
            new_image_file.seek(0)
            payload = {'image': new_image_file, 'product_id': self.product.id}
            res = self.client.post('/api/products/admin/image/product/', payload, **self.token_admin, fromat='multipart')

        self.product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(os.path.exists(old_path))
        self.assertTrue(os.path.exists(self.product.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        payload = {'iamge': 'string', 'product_id': self.product.id}
        res = self.client.post('/api/products/admin/image/product/', payload, **self.token_admin, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_unsuccess(self):
        """Test uploading image to a product unsuccess."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file, 'product_id': self.product.id}
            res = self.client.post('/api/products/admin/image/product/', payload, **self.token_user, fromat='multipart')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)