"""
Tests for the admin API.
"""
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import *


USER_URL = '/api/users/'
ADMIN_URL = '/api/users/admin/'
TOKEN_URL = reverse('user:user-token')

def get_token(path, params):
    """Create and return a token."""
    return path(TOKEN_URL, params)
def delete_user(id):
    return reverse('user:user-delete', args=(id,))
def get_user(id):
    return reverse('user:user', args=(id,))
def update_user_profile(id):
    return reverse('user:user-update', args=(id,))

def create_user(params, admin=False):
    """Create and return a new user."""
    if not admin:
        return User.objects.create_user(**params)
    else:
        return User.objects.create_superuser(**params)


class AdminUserAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.admin_payload = {
            'first_name': 'Admin Name',
            'email': 'admin@mail.com',
            'username': 'admin@mail.com',
            'password': 'password123',
        }
        self.admin = create_user(self.admin_payload, admin=True)

    def test_retrieve_profile_for_admin_user_success(self):
        """Test retrieving admin profile for valid token."""
        token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        admin_res = self.client.get(f'{USER_URL}details/profile/', **token, format='json')

        self.assertEqual(admin_res.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_res.data, {
            'id': self.admin.id,
            'username': self.admin.username,
            'email': self.admin.email,
            'name': self.admin.first_name,
            'isAdmin': True
        })

    def test_retrieve_all_users_success(self):
        """Test retrieving profiles for all users using a valid admin token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        create_user(payload)
        users = User.objects.all()
        token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        list_users_res = self.client.get(ADMIN_URL, **token, format='json')

        self.assertEqual(list_users_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_users_res.data), len(users))

    def test_unathorized_retrieve_all_users_unsuccess(self):
        """Test returns error if credentials invalid for admin."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        create_user(payload)
        token_res = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        list_users_res = self.client.get(ADMIN_URL, **token, format='json')

        self.assertEqual(list_users_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_profile_success(self):
        """Test retrieving profile for id user using valid admin token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        admin_token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {admin_token_res.data.get("token")}'}
        user_profile_res = self.client.get(f'{ADMIN_URL}{user.id}/', **token)

        self.assertEqual(user_profile_res.status_code, status.HTTP_200_OK)

    def test_retrieve_user_profile_unsuccess(self):
        """Test retrieving profile for id user using user token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        admin_token_res = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {admin_token_res.data.get("token")}'}
        user_profile_res = self.client.get(f'{ADMIN_URL}{user.id}/', **token)

        self.assertEqual(user_profile_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile_success(self):
        """Test update profile for id user using valid admin token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        admin_token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {admin_token_res.data.get("token")}'}
        updated_payload = {'email': 'updated@mail.com'}
        user_updated_profile_res = self.client.put(f'{ADMIN_URL}{user.id}/', updated_payload, **token, format='json')

        self.assertEqual(user_updated_profile_res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user_updated_profile_res.data['email'], payload['email'])

    def test_update_user_profile_unsuccess(self):
        """Test update profile for id user using invalid admin token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        admin_token_res = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {admin_token_res.data.get("token")}'}
        updated_payload = {'email': 'updated@mail.com'}
        user_updated_profile_res = self.client.put(f'{ADMIN_URL}{user.id}/', updated_payload, **token, format='json')

        self.assertEqual(user_updated_profile_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_success(self):
        """Test delete user using a valid admin token."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        delete_users_res = self.client.delete(f'{ADMIN_URL}{user.id}/', **token)
        user_exists = User.objects.filter(id=user.id).exists()

        self.assertEqual(delete_users_res.status_code, status.HTTP_200_OK)
        self.assertFalse(user_exists)

    def test_delete_user_not_exist_unsuccess(self):
        """Test delete user does not exist using a valid admin token."""
        token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        delete_users_res = self.client.delete(f'{ADMIN_URL}{self.admin.id+1}/', **token)

        self.assertEqual(delete_users_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_admin_unsuccess(self):
        """Test delete admin itself using valid admin token unsuccess."""
        token_res = get_token(self.client.post, self.admin_payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        delete_users_res = self.client.delete(f'{ADMIN_URL}{self.admin.id}/', **token)

        self.assertEqual(delete_users_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_unsuccess(self):
        """Test delete user using a valid user token unsuccess."""
        payload = {
                'first_name': 'Test Name',
                'email': 'test@mail.com',
                'username': 'test@mail.com',
                'password': 'password123',
            }
        user = create_user(payload)
        token_res = get_token(self.client.post, payload)
        token = {'HTTP_AUTHORIZATION': f'Bearer {token_res.data.get("token")}'}
        delete_users_res = self.client.delete(f'{ADMIN_URL}{self.admin.id}/', **token)
        user_exists = User.objects.filter(id=user.id).exists()

        self.assertEqual(delete_users_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(user_exists)