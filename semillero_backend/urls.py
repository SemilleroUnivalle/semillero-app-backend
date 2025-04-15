from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render


schema_view = get_schema_view(
   openapi.Info(
      title="Semillero API",
      default_version='v1',
      description="API para gestionar el semillero",
      contact=openapi.Contact(email="contact@semillero.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Vista para la página de bienvenida
def welcome_view(request):
    context = {
        'logo_path': 'images/logo.png',  # Ruta relativa desde la carpeta static
    }
    return render(request, 'welcome.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estudiante/', include('estudiante.urls')),
    path('acudiente/', include('acudiente.urls')),
    path('area/', include('area.urls')),
    path('asistencia/', include('asistencia.urls')),
    path('discapacidad/', include('discapacidad.urls')),
    path('eps/', include('eps.urls')),
    path('evaluacion_programa/', include('evaluacion_programa.urls')),
    path('grado_escolar/', include('grado_escolar.urls')),
    path('grupo/', include('grupo.urls')),
    path('historial_cambios/', include('historial_cambios.urls')),
    path('inscripcion/', include('inscripcion.urls')),
    path('modulo/', include('modulo.urls')),
    path('oferta_modulo/', include('oferta_modulo.urls')),
    path('pago/', include('pago.urls')),
    path('periodo_academico/', include('periodo_academico.urls')),
    path('seguimiento_academico/', include('seguimiento_academico.urls')),
    #path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', welcome_view, name='welcome'),
]
