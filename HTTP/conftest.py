import pytest
from datetime import date

# Configuración global de fixtures para las pruebas unitarias de los serializadores

@pytest.fixture
def test_user(db):
    """Fixture para crear un usuario de prueba de tipo estudiante."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username='test_user',
        password='password123',
        user_type='estudiante',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def acudiente_instance(db):
    from acudiente.models import Acudiente
    return Acudiente.objects.create(
        nombre_acudiente='Juan',
        apellido_acudiente='Perez',
        celular_acudiente='3001234567',
        email_acudiente='juan.perez@example.com'
    )

@pytest.fixture
def estudiante_instance(db, test_user, acudiente_instance):
    from estudiante.models import Estudiante
    return Estudiante.objects.create(
        user=test_user,
        nombre='Test',
        apellido='Estudiante',
        numero_documento='1234567890',
        email='test.estudiante@example.com',
        acudiente=acudiente_instance,
        ciudad_residencia='Cali',
        eps='Sura',
        grado='11',
        tipo_documento='TI',
        genero='Masculino',
        fecha_nacimiento=date(2008, 5, 15),
        telefono_fijo='3333333',
        celular='3007654321',
        departamento_residencia='Valle',
        comuna_residencia='17',
        direccion_residencia='Calle 123 #45-67',
        estamento='Estudiante'
    )

@pytest.fixture
def area_instance(db):
    from area.models import Area
    return Area.objects.create(
        nombre_area='Ciencias',
        estado_area=True
    )

@pytest.fixture
def categoria_instance(db):
    from categoria.models import Categoria
    return Categoria.objects.create(
        nombre='Semillero Basico',
        estado=True
    )

@pytest.fixture
def modulo_instance(db, categoria_instance, area_instance):
    from modulo.models import Modulo
    return Modulo.objects.create(
        nombre_modulo='Modulo Introductorio',
        descripcion_modulo='Introduccion a la ciencia',
        estado=True,
        id_categoria=categoria_instance,
        id_area=area_instance
    )

@pytest.fixture
def oferta_academica_instance(db):
    from oferta_academica.models import OfertaAcademica
    return OfertaAcademica.objects.create(
        nombre='Semestre 2026-I',
        fecha_inicio=date(2026, 2, 1),
        estado='inscripcion'
    )

@pytest.fixture
def oferta_categoria_instance(db, oferta_academica_instance, categoria_instance):
    from oferta_categoria.models import OfertaCategoria
    return OfertaCategoria.objects.create(
        id_oferta_academica=oferta_academica_instance,
        id_categoria=categoria_instance,
        precio_publico=50000.00,
        precio_privado=60000.00,
        fecha_finalizacion=date(2026, 6, 30),
        estado=True
    )

@pytest.fixture
def profesor_instance(db):
    from django.contrib.auth import get_user_model
    from profesor.models import Profesor
    User = get_user_model()
    prof_user = User.objects.create_user(
        username='prof_user',
        password='password123',
        user_type='profesor',
        first_name='Prof',
        last_name='Sor'
    )
    return Profesor.objects.create(
        user=prof_user,
        nombre='Profesor',
        apellido='Test',
        numero_documento='98765432',
        email='prof@example.com',
        ciudad_residencia='Cali',
        eps='Sura',
        tipo_documento='CC',
        genero='Masculino',
        fecha_nacimiento=date(1985, 10, 25),
        telefono_fijo='3333333',
        celular='3000000000',
        departamento_residencia='Valle',
        comuna_residencia='17',
        direccion_residencia='Calle 123',
        area_desempeño='Física',
        grado_escolaridad='Magister'
    )

@pytest.fixture
def monitor_academico_instance(db):
    from django.contrib.auth import get_user_model
    from monitor_academico.models import MonitorAcademico
    User = get_user_model()
    mon_user = User.objects.create_user(
        username='mon_user',
        password='password123',
        user_type='monitor_academico',
        first_name='Mon',
        last_name='Itor'
    )
    return MonitorAcademico.objects.create(
        user=mon_user,
        nombre='Monitor',
        apellido='Academico',
        numero_documento='12121212',
        email='monitor@example.com',
        ciudad_residencia='Cali',
        eps='Sura',
        tipo_documento='CC',
        genero='Masculino',
        fecha_nacimiento=date(1998, 5, 20),
        telefono_fijo='3333333',
        celular='3000000001',
        departamento_residencia='Valle',
        comuna_residencia='17',
        direccion_residencia='Calle 123',
        area_desempeño='Matemáticas'
    )

@pytest.fixture
def grupo_instance(db, profesor_instance, monitor_academico_instance, oferta_academica_instance):
    from grupo.models import Grupo
    return Grupo.objects.create(
        nombre='Grupo A',
        profesor=profesor_instance,
        monitor_academico=monitor_academico_instance,
        oferta_academica=oferta_academica_instance
    )

@pytest.fixture
def inscripcion_instance(db, estudiante_instance, modulo_instance, oferta_categoria_instance, grupo_instance):
    from inscripcion.models import Inscripcion
    return Inscripcion.objects.create(
        id_estudiante=estudiante_instance,
        id_modulo=modulo_instance,
        id_oferta_categoria=oferta_categoria_instance,
        grupo=grupo_instance,
        oferta_academica=oferta_categoria_instance.id_oferta_academica,
        tipo_vinculacion='Publico',
        terminos=True
    )
