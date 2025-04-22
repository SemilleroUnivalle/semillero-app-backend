from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradoEscolarViewSet

router = DefaultRouter()
router.register(r'grado',GradoEscolarViewSet, basename='GradoEscolar')

urlpatterns = [
    path('', include(router.urls)),
]