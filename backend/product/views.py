"""
Views for the product APIs
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Product doesn\'t exist!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

