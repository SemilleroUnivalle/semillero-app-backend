import pytest
from categoria.models import Categoria
from categoria.serializers import CategoriaSerializer

@pytest.mark.django_db
def test_serializador_categoria_valido():
    data = {
        'nombre': 'Robótica Básica',
        'estado': True
    }
    serializer = CategoriaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    cat = serializer.save()
    assert cat.id_categoria is not None
    assert cat.nombre == 'Robótica Básica'

    # Probar serialización
    serializer_read = CategoriaSerializer(instance=cat)
    assert serializer_read.data['nombre'] == 'Robótica Básica'
    assert serializer_read.data['estado'] is True

@pytest.mark.django_db
def test_serializador_categoria_invalido():
    data = {
        'nombre': ''
    }
    serializer = CategoriaSerializer(data=data)
    assert not serializer.is_valid()
    assert 'nombre' in serializer.errors
