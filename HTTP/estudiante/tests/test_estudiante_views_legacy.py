import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from estudiante.models import Estudiante
from cuenta.models import CustomUser

# Language: python

from estudiante.views import EstudianteViewSet  # relative import of the view to test

# Fixtures for users and estudiante profile
@pytest.fixture
def admin_user(db):
    user = CustomUser.objects.create(username='admin', password='pass', user_type='administrador')
    return user

@pytest.fixture
def profesor_user(db):
    user = CustomUser.objects.create(username='profesor', password='pass', user_type='profesor')
    return user

@pytest.fixture
def estudiante_user(db):
    user = CustomUser.objects.create(username='estudiante', password='pass', user_type='estudiante')
    return user

@pytest.fixture
def estudiante_profile(db, estudiante_user, acudiente_instance):
    from datetime import date
    estudiante = Estudiante.objects.create(
        user=estudiante_user,
        nombre='Estudiante',
        apellido='Legacy',
        numero_documento='12345',
        email='legacy@example.com',
        acudiente=acudiente_instance,
        ciudad_residencia='Bogota',
        eps='Compensar',
        grado='10',
        tipo_documento='TI',
        genero='Femenino',
        fecha_nacimiento=date(2009, 8, 10),
        telefono_fijo='2222222',
        celular='3151112233',
        departamento_residencia='Cundinamarca',
        comuna_residencia='N/A',
        direccion_residencia='Calle Falsa 123',
        estamento='Estudiante'
    )
    return estudiante

# Helper to build URL endpoints
def list_url():
    # Assuming router is configured with basename "estudiante"
    try:
        return reverse('estudiante-list')
    except:
        return '/estudiantes/'

def detail_url(pk):
    try:
        return reverse('estudiante-detail', args=[pk])
    except:
        return f'/estudiantes/{pk}/'

# Test: List estudiantes
@pytest.mark.django_db
def test_list_students(admin_user, profesor_user, estudiante_user):
    client = APIClient()

    # Admin user must be allowed
    client.force_authenticate(user=admin_user)
    response = client.get(list_url())
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

    # Profesor user must be allowed
    client.force_authenticate(user=profesor_user)
    response = client.get(list_url())
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

    # Estudiante user should not be allowed (for list action)
    client.force_authenticate(user=estudiante_user)
    response = client.get(list_url())
    assert response.status_code == status.HTTP_403_FORBIDDEN

# Test: Create estudiante
@pytest.mark.django_db
def test_create_student(admin_user, profesor_user, acudiente_instance):
    client = APIClient()
    data = {
        "numero_documento": "98765",
        "contrasena": "securepass",
        "acudiente": acudiente_instance.id_acudiente,
        "nombre": "Nuevo",
        "apellido": "Estudiante",
        "email": "nuevo@example.com",
        "ciudad_residencia": "Bogota",
        "eps": "Compensar",
        "grado": "10",
        "tipo_documento": "TI",
        "genero": "Femenino",
        "fecha_nacimiento": "2009-08-10",
        "telefono_fijo": "2222222",
        "celular": "3151112233",
        "departamento_residencia": "Cundinamarca",
        "comuna_residencia": "N/A",
        "direccion_residencia": "Calle Falsa 123",
        "estamento": "Estudiante",
        "is_active": True,
        "colegio": "Colegio Test",
        "discapacidad": False,
        "tipo_discapacidad": "Ninguna",
        "descripcion_discapacidad": "Ninguna"
    }
    # As admin user: should succeed
    client.force_authenticate(user=admin_user)
    response = client.post(list_url(), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # As profesor: allowed due to AllowAny registration policy
    client.force_authenticate(user=profesor_user)
    data["numero_documento"] = "98766"
    response = client.post(list_url(), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

# Test: Retrieve estudiante
@pytest.mark.django_db
def test_retrieve_student(estudiante_profile, estudiante_user, admin_user):
    client = APIClient()
    url = detail_url(estudiante_profile.id_estudiante)
    
    # As same estudiante; permission should allow retrieval.
    client.force_authenticate(user=estudiante_user)
    response = client.get(url)
    # Note: Due to duplicate retrieve methods, actual permission might vary.
    # Here expecting 200 if allowed.
    assert response.status_code == status.HTTP_200_OK

    # As admin: allowed
    client.force_authenticate(user=admin_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

# Test: Update estudiante
@pytest.mark.django_db
def test_update_student(estudiante_profile, estudiante_user, admin_user):
    client = APIClient()
    url = detail_url(estudiante_profile.id_estudiante)
    updated_data = {
        "numero_documento": "12345",  # keeping same
    }
    # As the owning estudiante
    client.force_authenticate(user=estudiante_user)
    response = client.patch(url, updated_data, format='json')
    # Expect 200 as permission [IsEstudiante | IsAdministrador] permits update
    assert response.status_code == status.HTTP_200_OK

    # As admin, update with partial data
    client.force_authenticate(user=admin_user)
    response = client.patch(url, {"numero_documento": "54321"}, format='json')
    assert response.status_code == status.HTTP_200_OK

# Test: Delete estudiante
@pytest.mark.django_db
def test_destroy_student(estudiante_profile, admin_user, profesor_user):
    client = APIClient()
    url = detail_url(estudiante_profile.id_estudiante)
    
    # As profesor, deletion should be forbidden.
    client.force_authenticate(user=profesor_user)
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # As admin, deletion should succeed: 204 No Content
    client.force_authenticate(user=admin_user)
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

