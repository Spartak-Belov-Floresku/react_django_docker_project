"""
URL mapping for product app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import *

app_name = 'product'

router = DefaultRouter()
router.register("", UserProductViewSet, basename="user-products")
router.register("user/reviews/product", UserReveiwProductSet, basename="user-reveiws-product")
router.register("admin", AdminProductViewSet, basename="admin-products")
router.register("admin/update/product", AdminUpdateProductViewSet, basename="admin-update-product")
router.register("admin/delete/product", AdminDeleteProductViewSet, basename="admin-delete-product")

urlpatterns = [path('', include(router.urls))]