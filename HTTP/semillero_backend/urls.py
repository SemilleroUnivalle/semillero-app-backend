from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from login.views import LoginView
from logout.views import LogoutView

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
    path('evaluacion_programa/', include('evaluacion_programa.urls')),
    path('grupo/', include('grupo.urls')),
    path('historial_cambios/', include('historial_cambios.urls')),
    path('matricula/', include('inscripcion.urls')),
    path('modulo/', include('modulo.urls')),
    path('pago/', include('pago.urls')),
    path('oferta_categoria/', include('oferta_categoria.urls')),
    path('categoria/', include('categoria.urls')),
    path('seguimiento_academico/', include('seguimiento_academico.urls')),
    path('oferta_academica/', include('oferta_academica.urls')),
    path('administrador/', include('administrador.urls')),
    path('profesor/', include('profesor.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recuperacion_contrasena/', include('recuperacion_contrasena.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', welcome_view, name='welcome'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
