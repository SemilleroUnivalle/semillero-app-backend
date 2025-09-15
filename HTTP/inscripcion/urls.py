from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InscripcionViewSet

router = DefaultRouter()
router.register(r'mat',InscripcionViewSet, basename='Matricula')

urlpatterns = [
    path('', include(router.urls)),
]