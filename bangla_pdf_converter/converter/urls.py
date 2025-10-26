from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PDFConversionViewSet

router = DefaultRouter()
router.register(r'conversions', PDFConversionViewSet, basename='conversion')

urlpatterns = [
    path('', include(router.urls)),
]