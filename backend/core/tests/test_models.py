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
    product = models.Product.objects.create(
        user=user,
        name='Sample product name',
        description='Sample product description',
        price=Decimal('5.50')
    )
    return product


class ModelTests(TestCase):
    """Test models."""

    def test_craete_user_with_email_successful(self):
        """Test creating a user wiyth an email is successful."""
        email = 'test@mail.com'
        password = 'testpass123'
        user = create_user(email=email, password=password)

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_email = [
            ['test1@MAIL.com', 'test1@mail.com'],
            ['Test2@mail.com', 'Test2@mail.com'],
            ['TEST3@MAIL.COM', 'TEST3@mail.com'],
            ['test4@mail.COM', 'test4@mail.com'],
        ]

        for email, expected in sample_email:
            user = create_user(username=expected, email=email)
            self.assertEqual(user.email, expected)

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

    def test_create_review(self):
        """Test creating a product's review is successful."""
        user = create_user()
        product = create_product(user)
        review = models.Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=5,
            comment='test comment'
        )
        self.assertEqual(review.user, user)
        self.assertEqual(review.product, product)
        self.assertTrue(user.review_set.filter(product=product).exists())
        self.assertTrue(product.review_set.filter(user=user).exists())
