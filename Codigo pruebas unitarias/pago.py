import pytest
from decimal import Decimal
from pago.serializers import PagoSerializer

@pytest.mark.django_db
def test_serializador_pago_valido(inscripcion_instance):
    data = {
        'id_inscripcion': inscripcion_instance.id_inscripcion,
        'monto': 50000.00,
        'referencia': 'REF-12345',
        'enlace_recibido_pdf': 'https://example.com/recibo.pdf'
    }
    serializer = PagoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    pago = serializer.save()
    assert pago.id_pago is not None
    assert pago.monto == Decimal('50000.00')

    serializer_read = PagoSerializer(instance=pago)
    assert serializer_read.data['referencia'] == 'REF-12345'
    assert serializer_read.data['monto'] == '50000.00'
