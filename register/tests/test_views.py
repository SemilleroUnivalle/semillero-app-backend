import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from register.models import Estudiante

User = get_user_model()

@pytest.mark.django_db
def test_vista_registro_inicial():
    client = APIClient()
    url = reverse('initial-register')
    data = {
        'Nombre': 'Juan',
        'Apellidos': 'Pérez',
        'NumeroIdentificacion': '1234567890',
        'CorreoElectronico':'JuanPrez@gmail.com'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Estudiante.objects.filter(NumeroIdentificacion='1234567890').exists()

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'NumeroIdentificacion' in response.data
