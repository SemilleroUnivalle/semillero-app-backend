from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonitorAcademicoViewSet

router = DefaultRouter()
router.register(r'mon',MonitorAcademicoViewSet, basename='monitor_academico')

urlpatterns = [
    path('', include(router.urls)),
]