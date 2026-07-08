import pytest
from area.models import Area
from area.serializers import AreaSerializer

@pytest.mark.django_db
def test_serializador_area_valido():
    data = {
        'nombre_area': 'Sistemas',
        'estado_area': True
    }
    serializer = AreaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    area = serializer.save()
    assert area.id_area is not None
    assert area.nombre_area == 'Sistemas'

    # Probar serialización
    serializer_read = AreaSerializer(instance=area)
    assert serializer_read.data['nombre_area'] == 'Sistemas'
    assert serializer_read.data['estado_area'] is True

@pytest.mark.django_db
def test_serializador_area_invalido():
    data = {
        'nombre_area': ''  # Obligatorio
    }
    serializer = AreaSerializer(data=data)
    assert not serializer.is_valid()
    assert 'nombre_area' in serializer.errors
