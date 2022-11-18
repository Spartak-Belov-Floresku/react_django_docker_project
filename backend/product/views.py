"""
Views for the product APIs
"""
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .products import products


class ProductViewSet(viewsets.ViewSet):

    @api_view(['GET'])
    def get_products(request):
        return JsonResponse(products, safe=False)

