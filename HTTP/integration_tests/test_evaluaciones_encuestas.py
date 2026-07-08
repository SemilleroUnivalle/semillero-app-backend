import pytest
from rest_framework.test import APIClient
from rest_framework import status
from encuesta_satisfaccion.models import EncuestaSatisfaccion

@pytest.fixture
def otro_estudiante_user(db):
    """Fixture para crear un segundo usuario de tipo estudiante."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username="otro_estudiante_test",
        password="passwordEstudiante123",
        user_type="estudiante",
        first_name="Otro",
        last_name="Estudiante"
    )

@pytest.fixture
def otro_estudiante_profile(db, otro_estudiante_user, acudiente_instance):
    """Fixture para crear el perfil del segundo estudiante."""
    from estudiante.models import Estudiante
    from datetime import date
    return Estudiante.objects.create(
        user=otro_estudiante_user,
        nombre="Otro",
        apellido="Estudiante",
        numero_documento="1122334455",
        email="otro@test.com",
        acudiente=acudiente_instance,
        ciudad_residencia="Cali",
        eps="Sura",
        grado="10",
        tipo_documento="TI",
        genero="Femenino",
        fecha_nacimiento=date(2009, 10, 10),
        celular="3125556677",
        departamento_residencia="Valle",
        comuna_residencia="16",
        direccion_residencia="Calle Falsa 123",
        estamento="Estudiante"
    )

@pytest.mark.django_db
def test_flujo_encuestas_de_satisfaccion(estudiante_instance, otro_estudiante_profile, inscripcion_instance, profesor_instance):
    """
    Prueba de integración: Valida que un estudiante pueda responder
    su propia encuesta de satisfacción, pero no la de otro estudiante.
    También valida que un profesor pueda ver el reporte de satisfacción.
    """
    # 1. Estudiante dueño de la inscripción responde la encuesta
    cliente_estudiante = APIClient()
    cliente_estudiante.force_authenticate(user=estudiante_instance.user)

    payload_encuesta = {
        "id_inscripcion": inscripcion_instance.id_inscripcion,
        "nota_modulo": 4.50,
        "nota_docente": 4.80,
        "nota_monitor": 4.00,
        "nota_estudiante": 4.20,
        "comentarios": "El curso fue excelente y el monitor muy atento."
    }

    # Un estudiante puede responder su propia encuesta (POST /encuesta_satisfaccion/encuesta/)
    response_respuesta = cliente_estudiante.post("/encuesta_satisfaccion/encuesta/", payload_encuesta, format="json")
    assert response_respuesta.status_code == status.HTTP_201_CREATED
    assert response_respuesta.data["comentarios"] == "El curso fue excelente y el monitor muy atento."
    assert EncuestaSatisfaccion.objects.filter(id_inscripcion=inscripcion_instance.id_inscripcion).exists()

    # 2. Otro estudiante intenta responder la misma encuesta (Acceso denegado, 403 Forbidden)
    cliente_otro_estudiante = APIClient()
    cliente_otro_estudiante.force_authenticate(user=otro_estudiante_profile.user)

    # Cambiado a la URL con sufijo de router
    response_respuesta_denegada = cliente_otro_estudiante.post("/encuesta_satisfaccion/encuesta/", payload_encuesta, format="json")
    assert response_respuesta_denegada.status_code == status.HTTP_403_FORBIDDEN
    assert "error" in response_respuesta_denegada.data
    assert response_respuesta_denegada.data["error"] == "No tienes permiso para responder esta encuesta."

    # 3. Profesor accede al reporte de encuestas de satisfacción (Acceso permitido, 200 OK)
    cliente_profesor = APIClient()
    cliente_profesor.force_authenticate(user=profesor_instance.user)

    response_reporte = cliente_profesor.get("/encuesta_satisfaccion/encuesta/reporte/")
    assert response_reporte.status_code == status.HTTP_200_OK
    # El reporte debería contener al menos la encuesta que acabamos de crear
    assert len(response_reporte.data) > 0
    assert float(response_reporte.data[0]["nota_modulo"]) == 4.50
