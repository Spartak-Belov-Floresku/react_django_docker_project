"""
URL mapping for order app.
"""
from django.urls import path

from order.views import *

app_name = 'order'

urlpatterns = [
    path('add/', addOrdersItems, name='orders-add'),
    path('<str:pk>/', getOrderById, name='user-order'),
]