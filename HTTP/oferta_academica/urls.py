from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfertaAcademicaViewSet

router = DefaultRouter()
router.register(r'ofer',OfertaAcademicaViewSet, basename='OfertaAcademica')

urlpatterns = [
    path('', include(router.urls)),
]