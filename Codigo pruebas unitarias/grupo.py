import pytest
from grupo.models import Grupo
from grupo.serializers import GrupoSerializer, GrupoListaSerializer

@pytest.mark.django_db
def test_serializador_grupo_valido(profesor_instance, monitor_academico_instance, oferta_academica_instance):
    data = {
        'nombre': 'Grupo B',
        'profesor': profesor_instance.id,
        'monitor_academico': monitor_academico_instance.id,
        'oferta_academica': oferta_academica_instance.id_oferta_academica
    }
    serializer = GrupoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    grupo = serializer.save()
    assert grupo.id is not None
    assert grupo.nombre == 'Grupo B'

    # Probar serialización
    serializer_read = GrupoSerializer(instance=grupo)
    assert serializer_read.data['nombre'] == 'Grupo B'

@pytest.mark.django_db
def test_serializador_lista_grupo(grupo_instance, inscripcion_instance):
    # Probar serialización de GrupoListaSerializer
    serializer = GrupoListaSerializer(instance=grupo_instance)
    assert serializer.data['nombre'] == grupo_instance.nombre
    assert serializer.data['total_estudiantes'] == 1
    assert len(serializer.data['estudiantes']) == 1
    assert serializer.data['estudiantes'][0]['nombre'] == 'Test'
