import pytest
from acudiente.models import Acudiente
from acudiente.serializers import AcudienteSerializer

@pytest.mark.django_db
def test_serializador_acudiente_valido():
    data = {
        'nombre_acudiente': 'Maria',
        'apellido_acudiente': 'Gomez',
        'tipo_documento_acudiente': 'CC',
        'numero_documento_acudiente': '987654321',
        'celular_acudiente': '3123456789',
        'email_acudiente': 'maria.gomez@example.com'
    }
    serializer = AcudienteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    acudiente = serializer.save()
    assert acudiente.id_acudiente is not None
    assert acudiente.nombre_acudiente == 'Maria'

    # Probar serialización
    serializer_read = AcudienteSerializer(instance=acudiente)
    assert serializer_read.data['nombre_acudiente'] == 'Maria'
    assert serializer_read.data['id_acudiente'] == acudiente.id_acudiente

@pytest.mark.django_db
def test_serializador_acudiente_invalido():
    data = {
        'nombre_acudiente': '',  # Campo obligatorio
        'email_acudiente': 'invalid-email'
    }
    serializer = AcudienteSerializer(data=data)
    assert not serializer.is_valid()
    assert 'nombre_acudiente' in serializer.errors
