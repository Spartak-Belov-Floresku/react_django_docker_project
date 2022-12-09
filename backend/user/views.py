"""
Views for the user APIs
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


@api_view(['POST'])
def registerUser(request):
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
        
        user = User.objects.create(
            first_name=data['name'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this eamil already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserAddress(request):
    user = request.user
    address = UserAddress.objects.get(user__id=user.id)
    serializer = UserAddressSerializer(address, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createUserAddress(request):
    user = request.user
    data = request.data
    address = UserAddress.objects.filter(user__id=user.id).exists()
    if not address:
        user_address=UserAddress.objects.create(
            user=user,
            address=data['address'],
            city=data['city'],
            zipCode=data['zipCode'],
            )
        serializer = UserAddressSerializer(user_address, many=False)
        return Response(serializer.data)
    else:
        user_address=UserAddress.objects.get(user__id=user.id)
        user_address.address=data['address']
        user_address.city=data['city']
        user_address.zipCode=data['zipCode']
        user_address.save()
        user_address.refresh_from_db()
        serializer = UserAddressSerializer(user_address, many=False)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data  = request.data
    try:
        validate_email(data['email'])
    except:
        message = {'detail': 'Enter a valid email address.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if len(data['password']) > 0:
        password, message = validate_password(data['password'])
        if not password:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(data['password'])
    user.save()
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
