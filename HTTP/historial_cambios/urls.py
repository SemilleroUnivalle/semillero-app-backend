from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistorialCambiosViewSet

router = DefaultRouter()
router.register(r'his',HistorialCambiosViewSet, basename='HistorialCambios')

urlpatterns = [
    path('', include(router.urls)),
]