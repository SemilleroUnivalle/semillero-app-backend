import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from register.models import Estudiante

User = get_user_model()

@pytest.mark.django_db
def test_registro_inicial_e_inicio_sesion():
    client = APIClient()
    
    # Registro inicial
    url_registro = reverse('initial-register')
    data_registro = {
        'Nombre': 'Juan',
        'Apellidos': 'Pérez',
        'NumeroIdentificacion': '1234567890',
        'CorreoElectronico': 'JuanPerez@gmail.com'
    }
    response = client.post(url_registro, data_registro, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Estudiante.objects.filter(NumeroIdentificacion='1234567890').exists()

    # Inicio de sesión
    url_login = reverse('login')
    data_login = {
        'document_number': '1234567890',
        'password': '1234567890'
    }
    response = client.post(url_login, data_login, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    

@pytest.mark.django_db
def test_actualizacion_progresiva():
    client = APIClient()
    
    # Registro inicial
    url_registro = reverse('initial-register')
    estudiante_data = {
        'Nombre': 'Juan',
        'Apellidos': 'Pérez',
        'NumeroIdentificacion': '1234567890',
        'CorreoElectronico': 'JuanPerez@gmail.com'
    }
    response = client.post(url_registro, estudiante_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Estudiante.objects.filter(NumeroIdentificacion='1234567890').exists()

    # Inicio de sesión
    url_login = reverse('login')
    data_login = {
        'document_number': '1234567890',
        'password': '1234567890'
    }
    response = client.post(url_login, data_login, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    # Obtener el token de acceso
    access_token = response.data['access']
    print("Access Token:", access_token)  # Imprimir el token de acceso
    
    # Configurar el encabezado de autorización con el token Bearer
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    # Obtener la instancia del estudiante desde la base de datos
    estudiante_instance = Estudiante.objects.get(NumeroIdentificacion='1234567890')
    url_actualizacion = reverse('progressive-update', kwargs={'pk': estudiante_instance.pk})

    data_actualizacion = {
        'ConfirmacionCorreo': 'nuevo.correo@example.com',
        'CiudadNacimiento': 'Ciudad Nueva'
    }
    response = client.patch(url_actualizacion, data_actualizacion, format='json')
    assert response.status_code == status.HTTP_200_OK
    estudiante_instance.refresh_from_db()
    assert estudiante_instance.ConfirmacionCorreo == 'nuevo.correo@example.com'
    assert estudiante_instance.CiudadNacimiento == 'Ciudad Nueva'
