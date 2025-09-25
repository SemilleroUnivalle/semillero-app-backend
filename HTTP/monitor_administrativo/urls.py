from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonitorAdministrativoViewSet

router = DefaultRouter()
router.register(r'mon',MonitorAdministrativoViewSet, basename='monitor_administrativo')

urlpatterns = [
    path('', include(router.urls)),
]
