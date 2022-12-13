"""b
backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/users/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('api/products/', include('product.urls')),
    path('api/orders/', include('order.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
