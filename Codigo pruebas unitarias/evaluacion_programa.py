import pytest
from decimal import Decimal
from evaluacion_programa.serializers import EvaluacionProgramaSerializer

@pytest.mark.django_db
def test_serializador_evaluacion_programa_valido(inscripcion_instance):
    data = {
        'id_inscripcion': inscripcion_instance.id_inscripcion,
        'nota_metodologia': 4.50,
        'nota_estudiante': 4.00,
        'nota_profesor': 4.80,
        'nota_monitor': 3.90,
        'observaciones': 'Todo excelente'
    }
    serializer = EvaluacionProgramaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    eval_p = serializer.save()
    assert eval_p.id_evaluacion is not None
    assert eval_p.nota_metodologia == Decimal('4.50')

    # Probar serialización
    serializer_read = EvaluacionProgramaSerializer(instance=eval_p)
    assert serializer_read.data['nota_metodologia'] == '4.50'
    assert serializer_read.data['observaciones'] == 'Todo excelente'
