import pytest
from inscripcion.serializers import InscripcionEstudianteSoloSerializer, InscripcionSerializer, InscripcionInfProfeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_serializador_inscripcion_estudiante_solo(inscripcion_instance):
    serializer = InscripcionEstudianteSoloSerializer(instance=inscripcion_instance)
    assert serializer.data['id_estudiante']['nombre'] == 'Test'
    assert serializer.data['periodo']['nombre'] == 'Semestre 2026-I'

@pytest.mark.django_db
def test_serializador_inscripcion_valido(estudiante_instance, modulo_instance, oferta_categoria_instance, grupo_instance):
    data = {
        'id_estudiante': estudiante_instance.id_estudiante,
        'id_modulo': modulo_instance.id_modulo,
        'id_oferta_categoria': oferta_categoria_instance.id_oferta_categoria,
        'grupo': grupo_instance.id,
        'tipo_vinculacion': 'Privado',
        'terminos': True,
        'observaciones': 'Prueba inscripcion',
        'estado': 'No revisado'
    }
    serializer = InscripcionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    ins = serializer.save()
    assert ins.id_inscripcion is not None

    serializer_read = InscripcionSerializer(instance=ins)
    assert serializer_read.data['tipo_vinculacion'] == 'Privado'
    assert serializer_read.data['estudiante']['nombre'] == 'Test'

@pytest.mark.django_db
def test_serializador_inscripcion_informacion_profesor(inscripcion_instance):
    serializer = InscripcionInfProfeSerializer(instance=inscripcion_instance)
    assert serializer.data['profesor']['nombre'] == 'Profesor'
    assert serializer.data['tipo_vinculacion'] == 'Publico'
