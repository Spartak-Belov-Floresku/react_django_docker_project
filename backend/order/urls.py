"""
URL mapping for order app.
"""
from django.urls import path

from order.views import *

app_name = 'order'

urlpatterns = [
    path('', getOrders, name='orders'),
    path('add/', addOrdersItems, name='orders-add'),
    path('myorders/', getMyOrders, name='myorders'),
    path('<str:pk>/deliver/', updateOrderToDelivered, name='order-delivered'),
    path('<str:pk>/', getOrderById, name='user-order'),
    path('<str:pk>/pay/', updateOrderToPaid, name='pay'),
]