import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')
django.setup()

from datetime import date
from oferta_academica.models import OfertaAcademica
from grupo.models import Grupo
from grupo.views import GrupoViewSet
from rest_framework.test import APIRequestFactory

def run_test():
    print("Iniciando prueba de creación de grupo...")
    # 1. Asegurarnos que haya una OfertaAcadémica activa.
    oferta_activa = OfertaAcademica.objects.filter(estado__in=['inscripcion', 'desarrollo']).order_by('-id_oferta_academica').first()
    
    if not oferta_activa:
        print("No hay oferta académica activa. Creando una de prueba...")
        oferta_activa = OfertaAcademica.objects.create(
            nombre="Periodo de Prueba 2026-Test",
            fecha_inicio=date.today(),
            estado="inscripcion"
        )
        print(f"-> Oferta creada: {oferta_activa}")
    else:
        print(f"-> Usando oferta académica activa existente: {oferta_activa.nombre} (ID: {oferta_activa.id_oferta_academica})")

    # 2. Emulamos la petición POST para crear un grupo (sin especificar la oferta)
    factory = APIRequestFactory()
    url = '/grupo/'
    # Pasamos solo el nombre para probar que el serializer lo acepta y la vista le asigna la oferta
    data = {"nombre": "Grupo_Test_Auto"} 
    
    request = factory.post(url, data, format='json')
    
    # Necesitamos autenticar para evitar el 401, creamos/buscamos un admin
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.first() # Si no hay admin, tomamos el primero
        
    from rest_framework.test import force_authenticate
    force_authenticate(request, user=admin_user)

    # Forzamos la asignacion de user si fuera necesario, pero la vista probablemente necesite request.data
    # Usaremos el view para el metodo create
    view = GrupoViewSet.as_view({'post': 'create'})
    
    print(f"\nSimulando la petición POST al endpoint de grupos con datos incompletos: {data}")
    
    try:
        # En una prueba real DRF podría quejarse de autenticación u objeto de request no estándar, 
        # así que deshabilitamos algunas clases por si acaso de manera temporal para la simulación
        view_instance = view.cls()
        view_instance.request = request
        view_instance.format_kwarg = None
        
        response = view(request)
        print(f"\nRespuesta de la API (Status): {response.status_code}")
        print(f"Respuesta de la API (Datos): {response.data}")
        
        if response.status_code == 201:
            grupo_creado = Grupo.objects.get(id=response.data.get('id', response.data.get('id_grupo', response.data.get('id_grupo', Grupo.objects.last().id))))
            print(f"\n✅ ¡Éxito! El grupo se guardó en la base de datos.")
            print(f"-> Nombre del grupo: '{grupo_creado.nombre}'")
            print(f"-> Oferta asiganada automáticamente: '{grupo_creado.oferta_academica.nombre}'")
            
            # Limpiamos el grupo de prueba
            print("\nLimpiando (eliminando) este grupo de prueba para no generar basura...")
            grupo_creado.delete()
            print("Limpieza completada.")
        else:
             print("\n❌ Hubo un fallo en la validación o guardado.")
             
    except Exception as e:
        print(f"\n❌ Oops, ocurrió un error en la simulación: {e}")

if __name__ == '__main__':
    run_test()
