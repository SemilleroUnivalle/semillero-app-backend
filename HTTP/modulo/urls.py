from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuloViewSet

router = DefaultRouter()
router.register(r'mod',ModuloViewSet, basename='Modulo')

urlpatterns = [
    path('', include(router.urls)),
]