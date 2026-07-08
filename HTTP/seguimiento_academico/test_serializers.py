import pytest
from decimal import Decimal
from seguimiento_academico.serializers import SeguimientoAcademicoSerializer

@pytest.mark.django_db
def test_serializador_seguimiento_academico_valido(inscripcion_instance):
    data = {
        'id_inscripcion': inscripcion_instance.id_inscripcion,
        'seguimiento_1': 4.50,
        'seguimiento_2': 4.00,
        'nota_conceptual_docente': 4.80,
        'nota_conceptual_estudiante': 4.20,
        'observaciones': 'Cumplió todas las metas'
    }
    serializer = SeguimientoAcademicoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    seg = serializer.save()
    assert seg.id_seguimiento is not None
    assert seg.nota_final == (Decimal('4.50') * Decimal('0.3') + 
                              Decimal('4.00') * Decimal('0.3') + 
                              Decimal('4.80') * Decimal('0.2') + 
                              Decimal('4.20') * Decimal('0.2'))

    # Probar la serialización
    serializer_read = SeguimientoAcademicoSerializer(instance=seg)
    assert serializer_read.data['estudiante_nombre'] == 'Test'
    assert serializer_read.data['grupo_nombre'] == 'Grupo A'
    assert Decimal(serializer_read.data['nota_final']) > 0
