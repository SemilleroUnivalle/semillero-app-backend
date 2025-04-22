from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfertaModuloViewSet

router = DefaultRouter()
router.register(r'ofer',OfertaModuloViewSet, basename='OfertaModulo')

urlpatterns = [
    path('', include(router.urls)),
]