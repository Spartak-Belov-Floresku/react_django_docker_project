"""
Views for the user APIs
"""
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
# from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import *


def validate_password(password):
    """Function validates user password."""
    if len(password) < 8:
        return False, {'detail':'Password is too short!'}
    else:
        return True, {}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k]=v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterViewSet(ModelViewSet):
    """Register a new user"""

    serializer_class = UserSerializerWithToken
    queryset = User.objects.none()
    http_method_names = ['post', ]

    def create(self, request):
        data = request.data
        try:
            try:
                validate_email(data['email'])
            except:
                message = {'detail': 'Enter a valid email address.'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            password, message = validate_password(data['password'])
            if not password:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            user = self.queryset.create(
                first_name=data['name'],
                email=data['email'],
                password=make_password(data['password'])
            )
            serializer = self.serializer_class(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this eamil already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """Class to munipulation with authenticated user profile."""

    serializer_class = UserSerializer
    queryset = User.objects.none()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put',]

    def retrieve(self, request, pk=None):
        user = request.user
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)

    def update(self, request, pk=None):
        self.serializer_class = UserSerializerWithToken
        user = request.user
        serializer = self.serializer_class(user, many=False)
        data = request.data
        try:
            validate_email(data.get('email'))
        except:
            message = {'detail': 'Enter a valid email address.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        user.first_name = data.get('name')
        user.username = data.get('email')
        user.email = data.get('email')
        if len(data.get('password')) > 0:
            password, message = validate_password(data.get('password'))
            if not password:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(data.get('password'))
        user.save()

        return Response(serializer.data)


class UserAddressViewSet(ModelViewSet):
    """User address with athenticated user."""

    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post',]

    def retrieve(self, request, pk=None):
        user = request.user
        try:
            address = self.queryset.get(user__id=user.id)
            serializer = self.serializer_class(address, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'The user doesn\'t have an address.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        address = self.queryset.filter(user__id=user.id).exists()
        if not address:
            user_address=self.queryset.create(
                user=user,
                address=data['address'],
                city=data['city'],
                zipCode=data['zipCode'],
                )
            serializer = self.serializer_class(user_address, many=False)
            return Response(serializer.data)
        else:
            user_address=self.queryset.get(user__id=user.id)
            user_address.address=data['address']
            user_address.city=data['city']
            user_address.zipCode=data['zipCode']
            user_address.save()
            user_address.refresh_from_db()
            serializer =  self.serializer_class(user_address, many=False)
            return Response(serializer.data)


class AdminUserViewSet(ModelViewSet):
    """Admin access to user data."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ['get', 'put', 'delete',]

    def list(self, request):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = self.queryset.get(id=pk)
            serializer = self.serializer_class(user, many=False)
            return Response(serializer.data)
        except:
            return Response({'detail': f'User with id {pk} does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.queryset.get(id=pk)
        data  = request.data
        user.first_name = data.get('name', user.first_name)

        try:
            validate_email(data.get('email'))
            user.username = data.get('email')
            user.email = data.get('email')
        except:
            user.username = user.email
            user.email = user.email

        user.is_staff = data.get('isAdmin', False)

        if data.get('password', False):
            password, message = validate_password(data.get('password'))
            if not password:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(data.get('password'))

        user.save()
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        if str(user.id) != str(pk):
            try:
                userToDelete = self.queryset.get(id=pk)
                userToDelete.delete()
                return Response('User was deleted')
            except:
                return Response({'detail': f'User with id {pk} does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'The operation is not allowed.'}, status=status.HTTP_400_BAD_REQUEST)

