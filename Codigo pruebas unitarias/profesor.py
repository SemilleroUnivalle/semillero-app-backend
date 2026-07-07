import pytest
from profesor.serializers import ProfesorSerializer, ProfesorModuloSerializer, AsignacionProfesorSerializer, ProfesorMeSerializer, ProfesorSimpleSerializer
from profesor.models import Profesor
from cuenta.models import CustomUser

@pytest.mark.django_db
def test_serializador_profesor_valido():
    user = CustomUser.objects.create_user(username='prof_test_s', password='password123', user_type='profesor')
    data = {
        'user': user.id,
        'nombre': 'Luis',
        'apellido': 'Perez',
        'numero_documento': '12341234',
        'email': 'luis@example.com',
        'ciudad_residencia': 'Cali',
        'eps': 'Sura',
        'tipo_documento': 'CC',
        'genero': 'Masculino',
        'fecha_nacimiento': '1990-09-12',
        'telefono_fijo': '3333333',
        'celular': '3102222222',
        'departamento_residencia': 'Valle',
        'comuna_residencia': '17',
        'direccion_residencia': 'Calle 10 #2-3',
        'area_desempeño': 'Física',
        'grado_escolaridad': 'Magister'
    }
    serializer = ProfesorSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    prof = serializer.save()
    assert prof.id is not None
    assert prof.nombre == 'Luis'

    serializer_read = ProfesorSerializer(instance=prof)
    assert serializer_read.data['nombre'] == 'Luis'

@pytest.mark.django_db
def test_serializador_asignacion_profesor_valido(profesor_instance, modulo_instance):
    data = {
        'id': profesor_instance.id,
        'id_modulo': modulo_instance.id_modulo
    }
    serializer = AsignacionProfesorSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_serializador_asignacion_profesor_invalido():
    data = {
        'id': 9999,
        'id_modulo': 9999
    }
    serializer = AsignacionProfesorSerializer(data=data)
    assert not serializer.is_valid()
