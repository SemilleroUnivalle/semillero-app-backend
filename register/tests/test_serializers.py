import pytest
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.contrib.auth import get_user_model
from register.models import Estudiante
from register.serializers import InitialRegistrationSerializer, ProgressiveUpdateSerializer, EstudianteSerializer

User = get_user_model()

@pytest.mark.django_db
def test_serializador_registro_inicial():
    data = {
        'Nombre': 'Juan',
        'Apellidos': 'Pérez',
        'NumeroIdentificacion': '1234567890',
        'CorreoElectronico': 'JuanPerez@gmail.com'
    }
    serializer = InitialRegistrationSerializer(data=data)
    assert serializer.is_valid()
    estudiante = serializer.save()
    assert estudiante.Nombre == 'Juan'
    assert estudiante.Apellidos == 'Pérez'
    assert estudiante.NumeroIdentificacion == '1234567890'
    assert estudiante.user.document_number == '1234567890'

    # Verificar que se lanza una ValidationError si el NumeroIdentificacion ya está en uso
    with pytest.raises(DRFValidationError):
        serializer = InitialRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)



