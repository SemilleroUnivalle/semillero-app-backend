from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  # Automatically generates CRUD routes

urlpatterns = [
    path('', include(router.urls)),  # Includes all DRF-generated URLs
]
