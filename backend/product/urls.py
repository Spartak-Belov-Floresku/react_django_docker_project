"""
URL mapping for product app.
"""
from django.urls import (
    path,
    include,
)

from product.views import ProductViewSet

app_name = 'product'

urlpatterns = [
    path('', ProductViewSet.get_products, name='products'),
]