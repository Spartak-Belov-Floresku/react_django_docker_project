"""
URL mapping for product app.
"""
from django.urls import path

from product.views import *

app_name = 'product'

urlpatterns = [
    path('', getProducts, name='products'),
    path('<str:pk>', getProduct, name='product'),
]