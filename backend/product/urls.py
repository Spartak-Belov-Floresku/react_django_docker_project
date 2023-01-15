"""
URL mapping for product app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import *

app_name = 'product'

router = DefaultRouter()
router.register("user", UserProductViewSet, basename="user-products")
router.register("user/reviews", UserReveiwProductSet, basename="user-reveiws-product")
router.register("admin", AdminProductViewSet, basename="admin-products")

urlpatterns = [path('', include(router.urls))]