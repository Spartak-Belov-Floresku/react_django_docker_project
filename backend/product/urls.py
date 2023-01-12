"""
URL mapping for product app.
"""
from django.urls import path

from product.views import *

app_name = 'product'

urlpatterns = [
    path('', Products.as_view({'get': 'get_products'}), name='products'),

    path('admin/products/', AdminProducts.as_view({'get': 'get_products'}), name='admin-products'),
    path('admin/upload/image/', AdminProducts.as_view({'post': 'upload_image'}), name='admin-upload-image'),

    path('<str:pk>/reviews/', UserProduct.as_view({'post': 'create_product_review'}), name='create-review'),
    path('top/', Products.as_view({'get': 'get_top_products'}), name='top-products'),
    path('<str:pk>/', Products.as_view({'get': 'get_product'}), name='product'),

    path('create/product/', AdminProducts.as_view({'post': 'create_product'}), name='create-product'),
    path('update/product/<str:pk>/', AdminProducts.as_view({'put': 'update_product'}), name='update-product'),
    path('delete/product/<str:pk>/', AdminProducts.as_view({'delete': 'delete_product'}), name='delete-product'),
]