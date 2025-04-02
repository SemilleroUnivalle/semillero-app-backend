from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentLoginView, StudentRegisterPhase2View,StudentUploadFilesView,StudentRegistrationStatusView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', StudentLoginView.as_view(), name='student-login'),
    path('complete/<int:student_id>', StudentRegisterPhase2View.as_view(), name='student-registration-phase2'),
    path('upload-files/<int:student_id>/', StudentUploadFilesView.as_view(), name='student-upload-files'),
    path('status-register/<int:student_id>/', StudentRegistrationStatusView.as_view(), name='student-registration-status')
]
