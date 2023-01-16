"""
Views for the product APIs
"""
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Product, Review
from .serializers import ProductSerializer, ProductImageSerializer

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class UserProductViewSet(ModelViewSet):
    """User access to the products."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', ]

    def list(self, request):
        query = request.query_params.get('keyword', False)
        products = self.queryset.filter(active=True, name__icontains=query) if query else Product.objects.filter(active=True)
        page = request.query_params.get('page')
        paginator = Paginator(products, 4)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        try:
            page = int(page)
        except:
            page = 1

        serializer = self.serializer_class(products, many=True)
        return Response({
                'products': serializer.data,
                'page': page,
                'pages': paginator.num_pages,
            })

    def retrieve(self, request, pk=None):
        try:
            product = self.queryset.get(id=pk)
            serializer =self.serializer_class(product, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'Product doesn\'t exist!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path=r'top')
    def top(self, request):
        products = self.queryset.filter(rating__gte=4, active=True).order_by('-rating')[0:5]
        serializer = self.serializer_class(products,many=True)
        return Response(serializer.data)


class UserReveiwProductSet(ModelViewSet):
    """User reviews the product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['patch', ]

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        product = self.queryset.get(id=pk)
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


class AdminProductViewSet(ModelViewSet):
    """Admin products class."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ['get', 'post', 'put', 'delete' ]

    def list(self, request):
        self.queryset = self.queryset.all()
        products = self.queryset.filter(active=False) if request.query_params.get('unactive', False) else self.queryset
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            user = request.user

            product = self.queryset.create(
                user=user,
                name='Sample Name',
                price=0,
                brand='Sample Brand',
                countInStock=0,
                category='Sample Category',
                description=''
            )

            serializer = self.get_serializer(product, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'Product cannot be created.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        product = self.queryset.get(id=pk)

        product.name = data.get('name')
        product.price = data.get('price')
        product.brand = data.get('brand')
        product.countInStock = data.get('countInStock')
        product.category = data.get('category')
        product.description = data.get('description')
        product.active = data.get('active') or False

        product.save()

        serializer = self.get_serializer(product, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path=r'image')
    def upload_image(self, request):

        data = request.data
        product_id = data['product_id']
        product = self.queryset.get(id=product_id)
        serializer = ProductImageSerializer(product, data=request.data)

        if serializer.is_valid():
            product.image.delete()
            product.image = request.FILES.get('image')
            product.save()
            return Response('Image was uploaded', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = self.queryset.get(id=pk)
        reviews = Review.objects.filter(product=product)
        if bool(len(reviews)):
            for review in reviews:
                review.delete()
        product.image.delete()
        product.delete()

        return Response('Product Deleted')
