import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def usuario_prueba_estudiante(db):
    """Fixture para crear un usuario y estudiante con credenciales conocidas."""
    from estudiante.models import Estudiante
    from acudiente.models import Acudiente
    
    # Crear acudiente requerido
    acudiente = Acudiente.objects.create(
        nombre_acudiente="Acudiente Prueba",
        apellido_acudiente="Test",
        celular_acudiente="3000000000",
        email_acudiente="acudiente@test.com"
    )
    
    # Crear CustomUser de Django con número de documento como username
    contrasena_plana = "claveEstudiante123"
    user = User.objects.create_user(
        username="1098765432",
        password=contrasena_plana,
        user_type="estudiante",
        first_name="Carlos",
        last_name="Gomez",
        email="carlos@test.com"
    )
    
    # Crear perfil estudiante
    from datetime import date
    estudiante = Estudiante.objects.create(
        user=user,
        numero_documento="1098765432",
        nombre="Carlos",
        apellido="Gomez",
        email="carlos@test.com",
        acudiente=acudiente,
        ciudad_residencia="Cali",
        eps="Sura",
        grado="10",
        tipo_documento="TI",
        genero="Masculino",
        fecha_nacimiento=date(2009, 8, 12),
        celular="3159876543",
        departamento_residencia="Valle",
        comuna_residencia="16",
        direccion_residencia="Carrera 45 # 12-34",
        estamento="Estudiante",
        is_active=True,
        discapacidad=False,
        tipo_discapacidad="Ninguna",
        descripcion_discapacidad="Ninguna"
    )
    
    return {
        "user": user,
        "contrasena": contrasena_plana,
        "estudiante": estudiante
    }

@pytest.mark.django_db
def test_autenticacion_login_exitoso(usuario_prueba_estudiante):
    """Valida el inicio de sesión exitoso con credenciales correctas."""
    client = APIClient()
    payload = {
        "numero_documento": usuario_prueba_estudiante["user"].username,
        "contrasena": usuario_prueba_estudiante["contrasena"]
    }
    
    response = client.post("/login/", payload, format="json")
    
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["tipo_usuario"] == "estudiante"
    assert response.data["id"] == usuario_prueba_estudiante["estudiante"].id_estudiante

@pytest.mark.django_db
def test_autenticacion_login_credenciales_invalidas(usuario_prueba_estudiante):
    """Valida el rechazo de inicio de sesión con contraseña incorrecta."""
    client = APIClient()
    payload = {
        "numero_documento": usuario_prueba_estudiante["user"].username,
        "contrasena": "claveEquivocada"
    }
    
    response = client.post("/login/", payload, format="json")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
    assert response.data["detail"] == "Credenciales inválidas"

@pytest.mark.django_db
def test_autenticacion_logout(usuario_prueba_estudiante):
    """Valida el cierre de sesión correcto eliminando el token activo."""
    client = APIClient()
    
    # Iniciar sesión para obtener el token
    payload = {
        "numero_documento": usuario_prueba_estudiante["user"].username,
        "contrasena": usuario_prueba_estudiante["contrasena"]
    }
    login_response = client.post("/login/", payload, format="json")
    token_key = login_response.data["token"]
    
    # Configurar la cabecera de autorización del cliente
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_key}")
    
    # Cerrar sesión
    logout_response = client.post("/logout/")
    assert logout_response.status_code == status.HTTP_200_OK
    assert logout_response.data["detail"] == "Logout exitoso"

@pytest.mark.django_db
def test_acceso_endpoint_protegido(usuario_prueba_estudiante):
    """Valida que un usuario sin token no pueda acceder a endpoints protegidos."""
    client = APIClient()
    
    # Intentar acceder a un endpoint que requiere autenticación
    # Por ejemplo, listar áreas (requiere autenticación)
    response = client.get("/area/are/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
