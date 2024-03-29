"""
URL mapping for user app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import *

app_name = 'user'

router = DefaultRouter()
router.register("admin", AdminUserViewSet, basename="admin-user")
router.register("register", UserRegisterViewSet, basename="register-user")
router.register("details", UserViewSet, basename="details-user")
router.register("address", UserAddressViewSet, basename="address-user")

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name='user-token'),
    path('', include(router.urls))
]