import pytest
from datetime import date
from oferta_academica.serializers import OfertaAcademicaSerializer
from oferta_academica.models import OfertaAcademica

@pytest.mark.django_db
def test_serializador_oferta_academica_valido():
    data = {
        'nombre': 'Periodo Academico 2026-II',
        'fecha_inicio': date(2026, 8, 1),
        'estado': 'inscripcion'
    }
    serializer = OfertaAcademicaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    oferta = serializer.save()
    assert oferta.id_oferta_academica is not None
    assert oferta.nombre == 'Periodo Academico 2026-II'

    serializer_read = OfertaAcademicaSerializer(instance=oferta)
    assert serializer_read.data['nombre'] == 'Periodo Academico 2026-II'
