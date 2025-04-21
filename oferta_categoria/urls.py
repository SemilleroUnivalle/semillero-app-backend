from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfertaCategoriaViewSet

router = DefaultRouter()
router.register(r'ofer',OfertaCategoriaViewSet, basename='OfertaCategoria')

urlpatterns = [
    path('', include(router.urls)),
]