"""
URL mapping for user app.
"""
from django.urls import path

from user.views import *

app_name = 'user'

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='user-token'),
    path('register/', registerUser, name='register'),
    path('profile/', getUserProfile, name='user-profile'),
    path('profile/update/', updateUserProfile, name='user-profile-update'),
    path('address/', getUserAddress, name='user-address'),
    path('address/create/', createUserAddress, name='user-address-create'),
    path('', getUsers, name='users'),
]