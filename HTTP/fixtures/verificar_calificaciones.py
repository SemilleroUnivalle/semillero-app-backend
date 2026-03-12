import os
import django
from django.contrib.auth import get_user_model
from profesor.models import Profesor
from inscripcion.models import Inscripcion
from seguimiento_academico.models import SeguimientoAcademico
from rest_framework.test import APIRequestFactory, force_authenticate
from seguimiento_academico.views import SeguimientoAcademicoViewSet

def verify_grading_system():
    print("=== Iniciando Verificación del Sistema de Calificaciones ===")
    
    # 1. Obtener un profesor de prueba (usaremos el documento 400 que creamos antes)
    User = get_user_model()
    try:
        user_profesor = User.objects.get(username="400")
        profesor = Profesor.objects.get(user=user_profesor)
        print(f"Profesor encontrado: {profesor.nombre} (ID: {profesor.numero_documento})")
    except Exception as e:
        print(f"Error: No se encontró el profesor de prueba. {e}")
        return

    # 2. Verificar si tiene estudiantes asignados
    inscripciones = Inscripcion.objects.filter(grupo__profesor=profesor)
    print(f"Estudiantes asignados al profesor: {inscripciones.count()}")
    
    if inscripciones.count() == 0:
        print("Error: El profesor no tiene estudiantes asignados para la prueba.")
        return

    factory = APIRequestFactory()
    viewset = SeguimientoAcademicoViewSet.as_view({'get': 'estudiantes_seguimiento', 'post': 'create'})

    # 3. PROBAR LISTADO (GET estudiantes-seguimiento)
    print("\n--- Probando Listado de Estudiantes ---")
    request_list = factory.get('/seguimiento_academico/seg/estudiantes-seguimiento/')
    force_authenticate(request_list, user=user_profesor)
    response_list = viewset(request_list)
    
    if response_list.status_code == 200:
        print(f"✅ ÉXITO: Listado obtenido. Total: {len(response_list.data)} estudiantes.")
        primer_estudiante = response_list.data[0]
        id_inscripcion = primer_estudiante['id_inscripcion']
        print(f"   Ejemplo: Estudiante {primer_estudiante['estudiante_nombre']} (Inscripción ID: {id_inscripcion})")
    else:
        print(f"❌ ERROR en listado: Status {response_list.status_code}")
        print(response_list.data)
        return

    # 4. PROBAR CALIFICACIÓN (POST create)
    print("\n--- Probando Guardado de Nota ---")
    data_nota = {
        "id_inscripcion": id_inscripcion,
        "seguimiento_1": 4.5,
        "seguimiento_2": 3.5,
        "nota_conceptual_docente": 4.0,
        "nota_conceptual_estudiante": 4.0,
        "observaciones": "Prueba de sistema automatizada"
    }
    
    request_post = factory.post('/seguimiento_academico/seg/', data_nota, format='json')
    force_authenticate(request_post, user=user_profesor)
    response_post = viewset(request_post)
    
    if response_post.status_code in [200, 201]:
        print("✅ ÉXITO: Nota guardada/actualizada correctamente.")
        print(f"   Nota Final calculada: {response_post.data['nota_final']}")
    else:
        print(f"❌ ERROR al guardar nota: Status {response_post.status_code}")
        print(f"   Detalles: {response_post.data}")

    # 5. VERIFICAR QUE OTRO PROFESOR NO PUEDE CALIFICAR
    print("\n--- Probando Seguridad (Otro profesor) ---")
    try:
        otro_user = User.objects.get(username="401")
        request_hack = factory.post('/seguimiento_academico/seg/', data_nota, format='json')
        force_authenticate(request_hack, user=otro_user)
        response_hack = viewset(request_hack)
        
        if response_hack.status_code == 403:
            print("✅ ÉXITO: El sistema bloqueó correctamente al profesor no autorizado.")
        else:
            print(f"⚠️ AVISO: Se esperaba 403 pero se obtuvo {response_hack.status_code}.")
    except:
        print("Omitiendo prueba de seguridad (no hay otro profesor disponible)")

    print("\n=== Verificación Finalizada ===")

if __name__ == "__main__":
    verify_grading_system()
