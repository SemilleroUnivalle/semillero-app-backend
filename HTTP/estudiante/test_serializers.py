import pytest
from datetime import date
from estudiante.models import Estudiante
from estudiante.serializers import EstudianteSerializer, EstudianteSerializerMatricula, EstudianteLista, LogEntrySerializer
from acudiente.models import Acudiente
from cuenta.models import CustomUser

@pytest.mark.django_db
def test_serializador_estudiante_valido(acudiente_instance):
    user = CustomUser.objects.create_user(username='stud_test', password='password123', user_type='estudiante')
    data = {
        'user': user.id,
        'nombre': 'Estudiante',
        'apellido': 'Prueba',
        'numero_documento': '99999999',
        'email': 'stud@example.com',
        'acudiente': acudiente_instance.id_acudiente,
        'ciudad_residencia': 'Bogota',
        'eps': 'Compensar',
        'grado': '10',
        'colegio': 'Colegio A',
        'tipo_documento': 'TI',
        'genero': 'Femenino',
        'fecha_nacimiento': date(2009, 8, 10),
        'telefono_fijo': '2222222',
        'celular': '3151112233',
        'departamento_residencia': 'Cundinamarca',
        'comuna_residencia': 'N/A',
        'direccion_residencia': 'Calle Falsa 123',
        'estamento': 'Estudiante'
    }
    # Al escribir, el acudiente se pasa como ID, pero el campo contiene instancias del modelo al leer (solo lectura)
    serializer = EstudianteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    estudiante = serializer.save(acudiente=acudiente_instance)
    assert estudiante.id_estudiante is not None

    # Probar serialización
    serializer_read = EstudianteSerializer(instance=estudiante)
    assert serializer_read.data['nombre'] == 'Estudiante'
    assert serializer_read.data['acudiente']['nombre_acudiente'] == 'Juan'

@pytest.mark.django_db
def test_serializador_lista_estudiante(estudiante_instance):
    serializer = EstudianteLista(instance=estudiante_instance)
    assert serializer.data['id_estudiante'] == estudiante_instance.id_estudiante
    assert serializer.data['nombre'] == estudiante_instance.nombre
    assert serializer.data['colegio'] == estudiante_instance.colegio
