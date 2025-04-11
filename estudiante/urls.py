from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet, EstadoInscripcionView, EstudianteInicioSesionView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'est',EstudianteViewSet, basename='estudiante')

urlpatterns = [
    path('', include(router.urls)),
    path('inicio/', EstudianteInicioSesionView.as_view(), name='estudiante-inicio-sesion'),
    path('estado-registro/<int:estudiante_id>/', EstadoInscripcionView.as_view(), name='estudiante-estado-registro'),
    path('cerrar/', LogoutView.as_view(), name='estudiante-cerrar-sesion'),
]
