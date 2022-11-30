"""
URL mapping for user app.
"""
from django.urls import path

from user.views import *

app_name = 'user'

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', getUserProfile, name='user-profile'),

]