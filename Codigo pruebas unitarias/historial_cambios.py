import pytest
from historial_cambios.serializers import HistorialCambiosSerializer

@pytest.mark.django_db
def test_serializador_historial_cambios_valido():
    data = {
        'id_inscripcion': 10,
        'tipo_cambio': 'Cambio Módulo',
        'motivo_cambio': 'Estudiante prefiere otro horario',
        'id_nueva_inscripcion': 10,
        'id_modulo_nuevo': 3,
        'id_periodo_aplazado': 0,
        'Observaciones': 'Ninguna'
    }
    serializer = HistorialCambiosSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    hist = serializer.save()
    assert hist.id_cambio is not None
    assert hist.tipo_cambio == 'Cambio Módulo'

    serializer_read = HistorialCambiosSerializer(instance=hist)
    assert serializer_read.data['tipo_cambio'] == 'Cambio Módulo'
