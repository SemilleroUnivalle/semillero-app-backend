import pytest
from asistencia.models import Asistencia
from asistencia.serializers import AsistenciaSerializer
from datetime import date

@pytest.mark.django_db
def test_serializador_asistencia_valido(inscripcion_instance):
    data = {
        'id_inscripcion_id': inscripcion_instance.id_inscripcion,
        'fecha_asistencia': date(2026, 6, 16),
        'estado_asistencia': 'Presente',
        'comentarios': 'Llegó a tiempo',
        'sesion': '1'
    }
    serializer = AsistenciaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    asistencia = serializer.save()
    assert asistencia.id_asistencia is not None
    assert asistencia.estado_asistencia == 'Presente'

    # Probar serialización
    serializer_read = AsistenciaSerializer(instance=asistencia)
    assert serializer_read.data['estado_asistencia'] == 'Presente'
    assert 'id_inscripcion' in serializer_read.data
    assert serializer_read.data['id_inscripcion']['id_estudiante']['nombre'] == 'Test'

@pytest.mark.django_db
def test_serializador_asistencia_invalido():
    data = {
        'estado_asistencia': 'Presente'
        # Faltan campos obligatorios
    }
    serializer = AsistenciaSerializer(data=data)
    assert not serializer.is_valid()
