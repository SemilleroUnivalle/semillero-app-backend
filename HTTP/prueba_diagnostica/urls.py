from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PruebaDiagnosticaViewSet,
    PreguntaDiagnosticaViewSet,
    RespuestaDiagnosticaViewSet
)

router = DefaultRouter()
router.register(r'pruebas', PruebaDiagnosticaViewSet, basename='prueba-diagnostica')
router.register(r'preguntas', PreguntaDiagnosticaViewSet, basename='pregunta-diagnostica')
router.register(r'respuestas', RespuestaDiagnosticaViewSet, basename='respuesta-diagnostica')

urlpatterns = [
    path('', include(router.urls)),
]
