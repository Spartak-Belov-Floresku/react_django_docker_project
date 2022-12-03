"""
URL mapping for user app.
"""
from django.urls import path

from user.views import *

app_name = 'user'

urlpatterns = [
    path('', getUsers, name='users'),
    path('login/', MyTokenObtainPairView.as_view(), name='user-token'),
    path('register/', registerUser, name='register'),
    path('profile/', getUserProfile, name='user-profile'),
]