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

def create_order(user):
    """Create and return an oredr"""
    order = models.Order.objects.create(
            user=user,
            paymentMethod='PayPal',
            shippingPrice=Decimal('2'),
            totalPrice=Decimal('5')
    )
    return order


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

    def test_create_order(self):
        """Test creating an order is successful."""
        user = create_user()
        order = models.Order.objects.create(
            user=user,
            paymentMethod='PayPal',
            shippingPrice=Decimal('2'),
            totalPrice=Decimal('5')
        )

        self.assertTrue(user.order_set.filter(createdAt=order.createdAt).exists())
        self.assertTrue(models.Order.objects.filter(user__id=user.id).count()==1)
        self.assertTrue(models.Order.objects.get(id=user.order_set.filter(createdAt=order.createdAt)[0].id))

    def test_create_order_item(self):
        """Test creating an order item is successful."""
        user = create_user()
        product = create_product(user)
        order = models.Order.objects.create(
            user=user,
            paymentMethod='PayPal',
            shippingPrice=Decimal('2'),
            totalPrice=Decimal('5')
        )
        models.OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=1,
        )

        self.assertTrue(models.OrderItem.objects.filter(order__id=user.order_set.filter(createdAt=order.createdAt)[0].id).count()==1)
        self.assertTrue(product.orderitem_set.filter(name=product.name).exists())
        self.assertTrue(order.orderitem_set.filter(order__id=user.order_set.filter(createdAt=order.createdAt)[0].id).exists())

    def test_create_shipping_address(self):
        """Test creating a shipping address is successful."""
        user = create_user()
        order = models.Order.objects.create(
            user=user,
            paymentMethod='PayPal',
            shippingPrice=Decimal('2'),
            totalPrice=Decimal('5')
        )
        shipping_address = models.ShippingAddress.objects.create(
            order=order,
            address='The First Street',
            city='Mars',
            zipCode='00001'
        )
        self.assertEqual(models.ShippingAddress.objects.get(id=order.shippingaddress.id).address, shipping_address.address)
        self.assertTrue(models.ShippingAddress.objects.get(order=user.order_set.filter(createdAt=order.createdAt)[0]).address == shipping_address.address)

