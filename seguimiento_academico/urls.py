from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeguimientoAcademicoViewSet

router = DefaultRouter()
router.register(r'seg',SeguimientoAcademicoViewSet, basename='SeguimientoAcademico')

urlpatterns = [
    path('', include(router.urls)),
]