"""
URL mapping for product app.
"""
from django.urls import path

from product.views import *

app_name = 'product'

urlpatterns = [
    path('', getProducts, name='products'),
    path('admin/products/', getProductsAdmin, name='admin-products'),
    path('admin/upload/image/', uploadImage, name='admin-upload-image'),

    path('<str:pk>/reviews/', createProductReview, name='create-review'),
    path('top/', getTopProducts, name='top-products'),
    path('<str:pk>/', getProduct, name='product'),

    path('create/product/', createProduct, name='create-product'),
    path('update/product/<str:pk>/', updateProduct, name='update-product'),
    path('delete/product/<str:pk>/', deleteProduct, name='delete-product'),
]