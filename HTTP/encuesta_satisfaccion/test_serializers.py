import pytest
from decimal import Decimal
from encuesta_satisfaccion.models import EncuestaSatisfaccion
from encuesta_satisfaccion.serializers import EncuestaSatisfaccionSerializer, EncuestaSatisfaccionListSerializer

@pytest.mark.django_db
def test_serializador_encuesta_satisfaccion_valido(inscripcion_instance):
    data = {
        'id_inscripcion': inscripcion_instance.id_inscripcion,
        'nota_modulo': 4.5,
        'nota_docente': 5.0,
        'nota_monitor': 3.8,
        'nota_estudiante': 4.0,
        'comentarios': 'Excelente curso'
    }
    serializer = EncuestaSatisfaccionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    encuesta = serializer.save()
    assert encuesta.id_encuesta is not None
    assert encuesta.nota_modulo == Decimal('4.5')

    # Probar serialización
    serializer_read = EncuestaSatisfaccionSerializer(instance=encuesta)
    assert serializer_read.data['nota_modulo'] == '4.5'
    assert serializer_read.data['documento'] == '1234567890'
    assert serializer_read.data['nombre'] == 'Test Estudiante'
    assert serializer_read.data['modulo'] == 'Modulo Introductorio'

@pytest.mark.django_db
def test_serializador_encuesta_satisfaccion_invalido_sin_notas(inscripcion_instance):
    # La lógica de validación espera que se proporcione al menos una nota
    data = {
        'id_inscripcion': inscripcion_instance.id_inscripcion,
        'comentarios': 'No puse notas'
    }
    serializer = EncuestaSatisfaccionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors

@pytest.mark.django_db
def test_serializador_lista_encuesta_satisfaccion(inscripcion_instance):
    encuesta = EncuestaSatisfaccion.objects.create(
        id_inscripcion=inscripcion_instance,
        nota_modulo=4.0,
        nota_docente=4.5
    )
    serializer = EncuestaSatisfaccionListSerializer(instance=encuesta)
    assert serializer.data['documento'] == '1234567890'
    assert serializer.data['nombre'] == 'Test Estudiante'
    assert serializer.data['nota_modulo'] == '4.0'
