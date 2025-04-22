from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluacionProgramaViewSet

router = DefaultRouter()
router.register(r'eval',EvaluacionProgramaViewSet, basename='EvaluacionPrograma')

urlpatterns = [
    path('', include(router.urls)),
]
