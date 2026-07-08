import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from asistencia.models import Asistencia
from seguimiento_academico.models import SeguimientoAcademico

@pytest.mark.django_db
def test_gestion_asistencias_y_calificaciones(profesor_instance, estudiante_instance, inscripcion_instance):
    """
    Prueba de integración: Valida que un profesor pueda registrar la asistencia
    y las notas académicas de un estudiante inscrito en su grupo,
    y que un estudiante no tenga permisos para modificar calificaciones.
    """
    # 1. Configurar profesor autenticado en el cliente
    cliente_profesor = APIClient()
    cliente_profesor.force_authenticate(user=profesor_instance.user)

    # 2. Registrar asistencia del estudiante por parte del profesor
    # El modelo Asistencia requiere: id_inscripcion, fecha, estado_asistencia
    payload_asistencia = {
        "id_inscripcion_id": inscripcion_instance.id_inscripcion,
        "fecha_asistencia": "2026-06-16",
        "estado_asistencia": "Asistio"
    }

    response_asistencia = cliente_profesor.post("/asistencia/asis/", payload_asistencia, format="json")
    assert response_asistencia.status_code == status.HTTP_201_CREATED
    assert Asistencia.objects.filter(id_inscripcion=inscripcion_instance.id_inscripcion).exists()

    # 3. Registrar notas del seguimiento académico
    # El modelo SeguimientoAcademico requiere: id_inscripcion y notas (se calcula la nota final)
    # Primero nos aseguramos de que el grupo de la inscripción pertenezca a este profesor
    # (El fixture inscripcion_instance ya viene con grupo_instance, pero asignamos el profesor de la prueba)
    grupo = inscripcion_instance.grupo
    grupo.profesor = profesor_instance
    grupo.save()

    payload_seguimiento = {
        "id_inscripcion": inscripcion_instance.id_inscripcion,
        "seguimiento_1": 5.00,
        "seguimiento_2": 4.00,
        "nota_conceptual_docente": 4.50,
        "nota_conceptual_estudiante": 4.50,
        "observaciones": "Excelente rendimiento general"
    }

    response_seguimiento = cliente_profesor.post("/seguimiento_academico/seg/", payload_seguimiento, format="json")
    assert response_seguimiento.status_code == status.HTTP_201_CREATED
    
    # Comprobar cálculo automático de nota final:
    # 5.0 * 0.3 + 4.0 * 0.3 + 4.5 * 0.2 + 4.5 * 0.2 = 1.5 + 1.2 + 0.9 + 0.9 = 4.50
    nota_final_esperada = Decimal("4.50")
    seguimiento_db = SeguimientoAcademico.objects.get(id_inscripcion=inscripcion_instance.id_inscripcion)
    assert seguimiento_db.nota_final == nota_final_esperada

    # 4. Intentar modificar calificaciones siendo el estudiante (Acceso denegado)
    cliente_estudiante = APIClient()
    cliente_estudiante.force_authenticate(user=estudiante_instance.user)

    # Intentar modificar el seguimiento creado mediante POST /seguimiento_academico/seg/
    payload_estudiante = {
        "id_inscripcion": inscripcion_instance.id_inscripcion,
        "seguimiento_1": 5.00
    }
    response_estudiante_cambio = cliente_estudiante.post("/seguimiento_academico/seg/", payload_estudiante, format="json")
    assert response_estudiante_cambio.status_code == status.HTTP_403_FORBIDDEN
