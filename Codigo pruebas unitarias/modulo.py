import pytest
from modulo.serializers import ModuloReadSerializer, ModuloReadIdNombreSerializer, ModuloProfesorSerializer, ModuloWriteSerializer

@pytest.mark.django_db
def test_serializador_modulo_lectura(modulo_instance):
    serializer = ModuloReadSerializer(instance=modulo_instance)
    assert serializer.data['nombre_modulo'] == 'Modulo Introductorio'
    assert serializer.data['id_categoria']['nombre'] == 'Semillero Basico'
    assert serializer.data['id_area']['nombre_area'] == 'Ciencias'

@pytest.mark.django_db
def test_serializador_modulo_lectura_id_nombre(modulo_instance):
    serializer = ModuloReadIdNombreSerializer(instance=modulo_instance)
    assert serializer.data['id_modulo'] == modulo_instance.id_modulo
    assert serializer.data['nombre_modulo'] == 'Modulo Introductorio'
    assert 'descripcion_modulo' not in serializer.data

@pytest.mark.django_db
def test_serializador_modulo_escritura_valido(categoria_instance, area_instance):
    data = {
        'nombre_modulo': 'Física 1',
        'descripcion_modulo': 'Conceptos de mecánica clásica',
        'estado_modulo': True,
        'id_categoria': categoria_instance.id_categoria,
        'id_area': area_instance.id_area
    }
    serializer = ModuloWriteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    mod = serializer.save()
    assert mod.id_modulo is not None
    assert mod.nombre_modulo == 'Física 1'
