import pytest
from rest_framework.test import APIClient
from rest_framework import status
from pago.models import Pago

@pytest.fixture
def administrador_user(db):
    """Fixture para crear un usuario administrador."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username="admin_user_test",
        password="passwordAdmin123",
        user_type="administrador",
        first_name="Admin",
        last_name="Test"
    )

@pytest.mark.django_db
def test_flujo_pagos_permisos_y_creacion(estudiante_instance, inscripcion_instance, administrador_user):
    """
    Prueba de integración: Valida que un estudiante pueda registrar un pago
    para su inscripción, pero no listar todos los pagos del sistema (restringido a admin).
    """
    # 1. Estudiante autenticado registra un pago
    cliente_estudiante = APIClient()
    cliente_estudiante.force_authenticate(user=estudiante_instance.user)

    payload_pago = {
        "id_inscripcion": inscripcion_instance.id_inscripcion,
        "monto": 50000.00,
        "referencia": "REF-987654",
        "enlace_recibido_pdf": "http://ejemplo.com/pago.pdf"
    }

    # Estudiantes y administradores pueden crear pagos (POST /pago/pago/)
    response_creacion = cliente_estudiante.post("/pago/pago/", payload_pago, format="json")
    assert response_creacion.status_code == status.HTTP_201_CREATED
    assert response_creacion.data["referencia"] == "REF-987654"
    assert Pago.objects.filter(referencia="REF-987654").exists()

    # 2. Estudiante intenta listar los pagos (Acceso denegado, requiere admin)
    response_listado_estudiante = cliente_estudiante.get("/pago/pago/")
    assert response_listado_estudiante.status_code == status.HTTP_403_FORBIDDEN

    # 3. Administrador autenticado lista los pagos (Acceso permitido)
    cliente_admin = APIClient()
    cliente_admin.force_authenticate(user=administrador_user)
    
    response_listado_admin = cliente_admin.get("/pago/pago/")
    assert response_listado_admin.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
