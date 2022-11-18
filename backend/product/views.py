"""
Views for the product APIs
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .products import products

@api_view(['GET'])
def getProducts(request):
    return Response(products)

@api_view(['GET'])
def getProduct(request, pk):
    for i in products:
        if i['_id'] == pk:
            return Response(i)

