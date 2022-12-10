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
REGESTER_USER_URL = reverse('user:register')
PROFILE_URL = reverse('user:user-profile')
UPDATE_PROFILE_URL = reverse('user:user-profile-update')
PROFILE_ALL_USERS_URL = reverse('user:users')
GET_USER_ADDRESS = reverse('user:user-address')
CREATE_USER_ADDRESS = reverse('user:user-address-create')

def create_user(params, admin=False):
    """Create and return a new user."""
    if not admin:
        return User.objects.create_user(**params)
    else:
        return User.objects.create_superuser(**params)

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
            'email': 'test@mail.com',
            'username': 'test@mail.com',
            'password': 'password123',
        }
        self.user = create_user(self.payload)


    def test_create_user_success(self):
        """Test creating a new user."""
        payload = {
            'name': 'Name',
            'email': 'test2@mail.com',
            'password': 'password123',
        }
        res = self.client.post(REGESTER_USER_URL, payload, format='json')
        user_exists = User.objects.filter(email__exact=payload['email']).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(user_exists)


    def test_create_user_invalid_email(self):
        """Test creating a new user with an invalid email."""
        payload = {
            'name': 'Name',
            'email': 'some_email',
            'password': 'password123',
        }
        res = self.client.post(REGESTER_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        """Test an error is returned if password less than 8 chars."""
        payload = {
            'email': 'test3@mail.com',
            'name': 'Test Name',
            'password': 'short',
        }
        res = self.client.post(REGESTER_USER_URL, payload)
        user_exists = User.objects.filter(email=payload['email']).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)


    def test_create_user_with_email_already_exists(self):
        """Test creating user with email that already exists"""
        res = self.client.post(REGESTER_USER_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'User with this eamil already exists')


    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        res = get_token(self.client.post, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """Test returns error if credentials invalid."""
        payload = {
            'email': 'none@mail.com',
            'password': 'testpassword',
            }
        res = get_token(self.client.post, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_user_profile_success(self):
        """Test update user profile."""
        res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': ''
        }

        res = self.client.put(UPDATE_PROFILE_URL, payload, **token, format='json')

        user = User.objects.get(email__exact=payload['email'])
        serializer = UserSerializer(user, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], serializer.data['id'])
        self.assertNotEqual(res.data['email'], self.payload['email'])


    def test_update_user_profile_password_success(self):
        """Test update user profile and password."""
        res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': 'password123Updated'
        }

        res = self.client.put(UPDATE_PROFILE_URL, payload, **token, format='json')
        user = User.objects.get(email__exact=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(user.password, make_password(payload['password']))


    def test_update_user_profile_with_short_password(self):
        """Test an error is returned if password less than 8 chars."""
        res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}
        payload= {
            'email': 'test_password@mail.com',
            'name': 'Update Name',
            'password': 'short'
        }

        res = self.client.put(UPDATE_PROFILE_URL, payload, **token, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_user_profile_with_invalid_email(self):
        """Test update user profile with an invalid email."""
        res = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res.data.get("token")}'}
        payload= {
            'email': 'update_email.com',
            'name': 'Update Name',
            'password': ''
        }

        res = self.client.put(UPDATE_PROFILE_URL, payload, **token, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unathorized_update_user_profile(self):
        """Test unathorized update user profile."""
        payload= {
            'email': 'update@email.com',
            'name': 'Update Name',
            'password': ''
        }
        res = self.client.put(UPDATE_PROFILE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_user_unathorized(self):
        """Test authentication is required for user."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_profile_success(self):
        """Test retrieving profile for valid token in user."""
        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}

        res2 = self.client.get(PROFILE_URL, **token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'name': self.user.first_name,
            'isAdmin': False
        })


    def test_retrieve_profile_for_admin_user_success(self):
        """Test retrieving admin profile for valid token in user."""
        payload = {
                'first_name': 'Admin Name',
                'email': 'admin@mail.com',
                'username': 'admin@mail.com',
                'password': 'password123',
            }
        admin_user = create_user(payload, True)
        res1 = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.get(PROFILE_URL, **token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, {
            'id': admin_user.id,
            'username': admin_user.username,
            'email': admin_user.email,
            'name': admin_user.first_name,
            'isAdmin': True
        })


    def test_retrieve_all_users_success(self):
        """Test retrieving profiles for all users using a valid admin token."""
        payload = {
                'first_name': 'Admin Name',
                'email': 'admin@mail.com',
                'username': 'admin@mail.com',
                'password': 'password123',
            }
        create_user(payload, True)
        users = User.objects.all()
        res1 = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.get(PROFILE_ALL_USERS_URL, **token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res2.data), len(users))


    def test_unathorized_retrieve_all_users(self):
        """Test returns error if credentials invalid for admin."""
        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.get(PROFILE_ALL_USERS_URL, **token)

        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_user_address(self):
        """Test get address related to user."""

        user_address = create_user_address({
            'user': self.user,
            'address': 'Test street',
            'city': 'Test City',
            'zipCode': '00000'
        })

        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.get(GET_USER_ADDRESS, **token)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data['address'], user_address.address)


    def test_get_user_address_unsuccess(self):
        """Test get address not exists."""

        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.get(GET_USER_ADDRESS, **token)

        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_user_address(self):
        """Test create address related to user."""
        user_address = {
            'address': 'Test street',
            'city': 'Test City',
            'zipCode': '00000'
        }
        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.post(CREATE_USER_ADDRESS, user_address, **token, format='json')

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data['address'], user_address['address'])


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

        res1 = get_token(self.client.post, self.payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {res1.data.get("token")}'}
        res2 = self.client.post(CREATE_USER_ADDRESS, updated_user_address, **token, format='json')

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_user_address.address, updated_user_address['address'])
        self.assertEqual(res2.data['address'], updated_user_address['address'])
