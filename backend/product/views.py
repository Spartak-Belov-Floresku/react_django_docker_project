"""
Views for the product APIs
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Product, Review
from .serializers import ProductSerializer, ProductImageSerializer


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword', False)
    products = Product.objects.filter(active=True, name__icontains=query) if query else Product.objects.filter(active=True)
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
    products = Product.objects.filter(active=False) if request.query_params.get('unactive', False) else Product.objects.all()
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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request):

    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    serializer = ProductImageSerializer(product, data=request.data)

    if serializer.is_valid():
        product.image.delete()
        product.image = request.FILES.get('image')
        product.save()
        return Response('Image was uploaded', status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):

    product = Product.objects.get(id=pk)
    product.image.delete()
    product.delete()

    return Response('Product Deleted')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    data = request.data

    # 1 - Review already exists
    if product.review_set.filter(user=user).exists():
        content = {'detail': 'Product already reviewed!'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2- No rating
    elif not data.get('rating', False):
        content = {'detail': 'Please select rating!'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data.get('rating'),
            comment=data.get('comment', None),
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Reviewed.')
