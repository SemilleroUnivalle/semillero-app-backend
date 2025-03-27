from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentLoginView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', StudentLoginView.as_view(), name='student-login'),
]
