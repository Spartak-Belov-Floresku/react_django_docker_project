"""
Views for the order APIs
"""
from tabnanny import check
from urllib import response
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from core.models import Product, Order, OrderItem, ShippingAddress
from product.serializers import ProductSerializer
from .serializers import *

from rest_framework import status
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrdersItems(request):
    user = request.user
    data = request.data
    try:
        orderItems = data['orderItems']
        if not orderItems or not len(orderItems):
            raise

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            zipCode=data['shippingAddress']['zipCode'],
        )

        for item in orderItems:
            product=Product.objects.get(id=item['product'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=item['qty'],
                price=item['price'],
                image=product.image.url,
            )

            product.countInStock -= orderItem.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail':'No order items'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view.'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail':'Order does not exists'}, status=status.HTTP_400_BAD_REQUEST)