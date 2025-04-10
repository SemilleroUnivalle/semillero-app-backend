from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    #path('api/', include('todo.urls')),
    path('student/', include('student.urls')),
    #path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', welcome_view, name='welcome'),

    path('semillero/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('semillero/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
