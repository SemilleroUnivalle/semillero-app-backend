import pytest
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from estudiante.models import Estudiante
from inscripcion.models import Inscripcion

@pytest.mark.django_db
def test_flujo_registro_e_inscripcion_estudiante(acudiente_instance, modulo_instance, grupo_instance, oferta_categoria_instance):
    """
    Prueba de integración: Valida el registro completo de un estudiante
    y su posterior inscripción a un módulo académico activo.
    """
    client = APIClient()

    # --- FASE 1: REGISTRO DEL ESTUDIANTE ---
    # Enviar datos de registro de estudiante al endpoint POST /estudiante/
    payload_estudiante = {
        "numero_documento": "1112223334",
        "contrasena": "claveEstudiante456",
        "acudiente": acudiente_instance.id_acudiente,
        "nombre": "Sofia",
        "apellido": "Torres",
        "email": "sofia.torres@test.com",
        "ciudad_residencia": "Cali",
        "eps": "Sura",
        "grado": "11",
        "tipo_documento": "TI",
        "genero": "Femenino",
        "fecha_nacimiento": "2008-11-20",
        "telefono_fijo": "3334455",
        "celular": "3124445555",
        "departamento_residencia": "Valle",
        "comuna_residencia": "17",
        "direccion_residencia": "Avenida 3N # 12-45",
        "estamento": "Estudiante",
        "is_active": True,
        "colegio": "Colegio Mayor",
        "discapacidad": False,
        "tipo_discapacidad": "Ninguna",
        "descripcion_discapacidad": "Ninguna"
    }

    # El registro de estudiantes tiene permiso AllowAny
    response_registro = client.post("/estudiante/est/", payload_estudiante, format="json")
    
    assert response_registro.status_code == status.HTTP_201_CREATED
    id_estudiante = response_registro.data["id"]
    
    # Comprobar que existe en la base de datos
    estudiante_db = Estudiante.objects.get(id_estudiante=id_estudiante)
    assert estudiante_db.nombre == "Sofia"
    assert estudiante_db.user.username == "1112223334"

    # --- FASE 2: INSCRIPCIÓN AL MÓDULO ---
    # Asociar la oferta categoría al módulo de la prueba
    modulo_instance.id_oferta_categoria.add(oferta_categoria_instance)

    # Para inscribirse, la oferta_categoria y la oferta_academica deben estar activas (estado=True)
    oferta_categoria = modulo_instance.id_oferta_categoria.get()
    oferta_categoria.estado = True
    oferta_categoria.save()

    oferta_academica = oferta_categoria.id_oferta_academica
    oferta_academica.estado = "inscripcion"  # el estado de la oferta es un string según el modelo
    oferta_academica.save()

    # Payload para la inscripción
    payload_inscripcion = {
        "id_estudiante": id_estudiante,
        "id_modulo": modulo_instance.id_modulo,
        "grupo": grupo_instance.id,
        "tipo_vinculacion": "Publico",
        "terminos": True
    }

    # La creación de inscripciones tiene permiso AllowAny según get_permissions()
    response_inscripcion = client.post("/inscripcion/", payload_inscripcion, format="json")
    
    assert response_inscripcion.status_code == status.HTTP_201_CREATED
    assert response_inscripcion.data["estudiante"]["id_estudiante"] == id_estudiante
    assert response_inscripcion.data["modulo"]["id_modulo"] == modulo_instance.id_modulo
    
    # Comprobar la existencia del registro de inscripción en base de datos
    id_inscripcion = response_inscripcion.data["id_inscripcion"]
    inscripcion_db = Inscripcion.objects.get(id_inscripcion=id_inscripcion)
    assert   inscripcion_db.id_estudiante.id_estudiante == id_estudiante
    assert inscripcion_db.id_modulo.id_modulo == modulo_instance.id_modulo
    assert inscripcion_db.grupo.id == grupo_instance.id
