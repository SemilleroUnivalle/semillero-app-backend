from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EPSViewSet

router = DefaultRouter()
router.register(r'eps',EPSViewSet, basename='EPS')

urlpatterns = [
    path('', include(router.urls)),
]
