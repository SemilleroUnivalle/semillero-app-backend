from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeriodoAcademicoViewSet

router = DefaultRouter()
router.register(r'per',PeriodoAcademicoViewSet, basename='PeriodoAcademico')

urlpatterns = [
    path('', include(router.urls)),
]