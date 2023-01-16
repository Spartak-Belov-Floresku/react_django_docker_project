"""
Tests for the user API.
"""
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import *

TOKEN_URL = reverse('user:user-token')
USER_URL = '/api/users/'
USER_ADDRESS = '/api/users/address/'

def create_user(params):
    """Create and return a new user."""
    return User.objects.create_user(**params)

def create_user_address(params):
    """Create and return a new user address."""
    return UserAddress.objects.create(**params)

def get_token(path, params):
    """Create and return a token."""
    return path(TOKEN_URL, params)


class UserAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'Test Name',
            'email': 'user1@mail.com',
            'username': 'user1@mail.com',
            'password': 'password123',
        }
        self.user = create_user(self.payload)

    def test_create_user_success(self):
        """Test creating a new user."""
        payload = {
            'name': 'Name',
            'email': 'user2@mail.com',
            'password': 'password123',
        }
        res_user = self.client.post(f'{USER_URL}register/', payload, format='json')
        user_exists = User.objects.filter(email__exact=payload['email']).exists()

        self.assertEqual(res_user.status_code, status.HTTP_200_OK)
        self.assertTrue(user_exists)

    def test_create_user_invalid_email(self):
        """Test creating a new user with an invalid email."""
        payload = {
            'name': 'Name',
            'email': 'some_email',
            'password': 'password123',
        }
        res_user = self.client.post(f'{USER_URL}register/', payload, format='json')

        self.assertEqual(res_user.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 8 chars."""
        payload = {
            'email': 'test3@mail.com',
            'name': 'Test Name',
            'password': 'short',
        }
        res_user = self.client.post(f'{USER_URL}register/', payload)
        user_exists = User.objects.filter(email=payload['email']).exists()

        self.assertEqual(res_user.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_user_with_email_already_exists(self):
        """Test creating user with email that already exists"""
        res_user = self.client.post(f'{USER_URL}register/', self.payload, format='json')

        self.assertEqual(res_user.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_user.data['detail'], 'User with this eamil already exists')

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        res_token = get_token(self.client.post, self.payload)

        self.assertIn('token', res_token.data)
        self.assertEqual(res_token.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test returns error if credentials invalid."""
        payload = {
            'email': 'none@mail.com',
            'password': 'testpassword',
            }
        res_token = get_token(self.client.post, payload)

        self.assertNotIn('token', res_token.data)
        self.assertEqual(res_token.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile_success(self):
        """Test get user profile."""
        res_token = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res_token.data.get("token")}'}
        res_user = self.client.get(f'{USER_URL}details/profile/', **token, format='json')

        self.assertEqual(res_user.status_code, status.HTTP_200_OK)
        self.assertEqual(res_user.data['email'], self.payload['email'])

    def test_retrieve_user_profile_unathorized(self):
        """Test authentication is required for user."""
        res = self.client.get(f'{USER_URL}details/profile/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile_success(self):
        """Test update user profile."""
        res_token = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res_token.data.get("token")}'}
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': ''
        }

        res_user = self.client.put(f'{USER_URL}details/profile/', payload, **token, format='json')
        user = User.objects.get(email__exact=payload['email'])
        serializer = UserSerializer(user, many=False)

        self.assertEqual(res_user.status_code, status.HTTP_200_OK)
        self.assertEqual(res_user.data['id'], serializer.data['id'])
        self.assertNotEqual(res_user.data['email'], self.payload['email'])

    def test_update_user_profile_password_success(self):
        """Test update user profile and password."""
        res_token = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res_token.data.get("token")}'}
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': 'password123Updated'
        }

        res_user = self.client.put(f'{USER_URL}details/profile/', payload, **token, format='json')
        user = User.objects.get(email__exact=payload['email'])

        self.assertEqual(res_user.status_code, status.HTTP_200_OK)
        self.assertTrue(user.password, make_password(payload['password']))

    def test_update_user_profile_with_short_password(self):
        """Test an error is returned if password less than 8 chars."""
        res_token = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res_token.data.get("token")}'}
        payload= {
            'email': 'test_password@mail.com',
            'name': 'Update Name',
            'password': 'short'
        }

        res_user = self.client.put(f'{USER_URL}details/profile/', payload, **token, format='json')

        self.assertEqual(res_user.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_profile_with_invalid_email(self):
        """Test update user profile with an invalid email."""
        token_res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        payload= {
            'email': 'update_email.com',
            'name': 'Update Name',
            'password': ''
        }

        user_update_res = self.client.put(f'{USER_URL}details/profile/', payload, **token, format='json')

        self.assertEqual(user_update_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unathorized_update_user_profile(self):
        """Test unathorized update user profile."""
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': ''
        }
        res = self.client.put(f'{USER_URL}details/profile/', payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_address(self):
        """Test get address related to user."""

        user_address = create_user_address({
            'user': self.user,
            'address': 'Test street',
            'city': 'Test City',
            'zipCode': '00000'
        })

        token_res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        user_address_res = self.client.get(USER_ADDRESS+'retrieve/', **token)

        self.assertEqual(user_address_res.status_code, status.HTTP_200_OK)
        self.assertEqual(user_address_res.data['address'], user_address.address)


    def test_get_user_address_unsuccess(self):
        """Test get address not exists."""

        token_res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        user_address_res = self.client.get(USER_ADDRESS+'retrieve/', **token)

        self.assertEqual(user_address_res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_user_address(self):
        """Test create address related to user."""
        user_address = {
            'address': 'Test street',
            'city': 'Test City',
            'zipCode': '00000'
        }
        token_res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        user_address_res = self.client.patch(USER_ADDRESS+'update/', user_address, **token, format='json')

        self.assertEqual(user_address_res.status_code, status.HTTP_200_OK)
        self.assertEqual(user_address_res.data['address'], user_address['address'])


    def test_update_user_address(self):
        """Test update existing address related to user."""
        old_user_address = create_user_address({
            'user': self.user,
            'address': 'Test street',
            'city': 'Test City',
            'zipCode': '00000'
        })

        updated_user_address = {
            'address': 'Updated street',
            'city': 'Updated City',
            'zipCode': '00000'
        }

        token_res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        user_updated_address_res = self.client.patch(USER_ADDRESS+'update/', updated_user_address, **token, format='json')

        self.assertEqual(user_updated_address_res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_user_address.address, updated_user_address['address'])
        self.assertEqual(user_updated_address_res.data['address'], updated_user_address['address'])
