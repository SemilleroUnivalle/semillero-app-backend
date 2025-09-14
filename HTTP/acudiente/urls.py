from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcudienteViewSet

router = DefaultRouter()
router.register(r'acu',AcudienteViewSet, basename='Acudiente')

urlpatterns = [
    path('', include(router.urls)),
]
