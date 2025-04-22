from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdministradorViewSet

router = DefaultRouter()
router.register(r'admin',AdministradorViewSet, basename='administrador')

urlpatterns = [
    path('', include(router.urls)),
]
