"""
Views for the product APIs
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from core.models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.filter(active=True)
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getProductsAdmin(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    try:
        user = request.user

        product = Product.objects.create(
            user=user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category='Sample Category',
            description=''

        )

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Product cannot be created.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)

    product.name = data.get('name')
    product.price = data.get('price')
    product.brand = data.get('brand')
    product.countInStock = data.get('countInStock')
    product.category = data.get('category')
    product.description = data.get('description')
    product.active = data.get('active') or False

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):

    product = Product.objects.get(id=pk)
    product.image.delete()
    product.delete()

    return Response('Product Deleted')

