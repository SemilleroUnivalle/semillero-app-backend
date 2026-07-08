import pytest
from discapacidad.models import Discapacidad
from discapacidad.serializers import DiscapacidadSerializer

@pytest.mark.django_db
def test_serializador_discapacidad_valido():
    # Nota: DiscapacidadSerializer contiene una discrepancia en extra_kwargs:
    # hace referencia a 'nombre' y 'descripcion' en lugar de 'tipo_discapacidad' y 'info_discapacidad'.
    # Probaremos usando los campos reales del modelo para ver cómo se comporta el serializador.
    data = {
        'tipo_discapacidad': 'Visual',
        'info_discapacidad': 'Baja visión'
    }
    serializer = DiscapacidadSerializer(data=data)
    # Si la discrepancia en extra_kwargs causa una falla de inicialización/validación, esto fallará.
    assert serializer.is_valid(), serializer.errors
    disc = serializer.save()
    assert disc.id_discapacidad is not None
    assert disc.tipo_discapacidad == 'Visual'

    serializer_read = DiscapacidadSerializer(instance=disc)
    assert serializer_read.data['tipo_discapacidad'] == 'Visual'
