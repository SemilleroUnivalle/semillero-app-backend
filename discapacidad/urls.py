from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscapacidadViewSet

router = DefaultRouter()
router.register(r'dis',DiscapacidadViewSet, basename='Discapacidad')

urlpatterns = [
    path('', include(router.urls)),
]
