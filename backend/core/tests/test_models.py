"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from core import models


def create_user(admin=False, **params):
    """Create and return a new user."""
    defaults = {
        'username': 'test@mail.com',
        'email': 'test@mail.com',
        'password': 'password123',
    }
    defaults.update(params)

    if not admin:
        return User.objects.create_user(**defaults)
    else:
        return User.objects.create_superuser(**defaults)


class ModelTests(TestCase):
    """Test models."""

    def test_create_product(self):
        """Test creating a product is successful."""
        user = create_user()
        product = models.Product.objects.create(
            user=user,
            name='Sample product name',
            description='Sample product description',
            price=Decimal('5.50')
        )

        self.assertEqual(str(product), product.name)

    @patch('core.models.uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.products_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'products/{uuid}.jpg')