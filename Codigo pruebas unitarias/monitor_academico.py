import pytest
from monitor_academico.serializers import MonitorAcademicoSerializer, MonitorAcademicoModuloSerializer, AsignacionMonitorAcademicoSerializer
from monitor_academico.models import MonitorAcademico
from cuenta.models import CustomUser

@pytest.mark.django_db
def test_serializador_monitor_academico_valido():
    user = CustomUser.objects.create_user(username='mon_test', password='password123', user_type='monitor_academico')
    data = {
        'user': user.id,
        'nombre': 'Andres',
        'apellido': 'Lopez',
        'numero_documento': '12345678',
        'email': 'andres@example.com',
        'ciudad_residencia': 'Cali',
        'eps': 'Sura',
        'tipo_documento': 'CC',
        'genero': 'Masculino',
        'fecha_nacimiento': '1998-05-20',
        'telefono_fijo': '3333333',
        'celular': '3200000000',
        'departamento_residencia': 'Valle',
        'comuna_residencia': '17',
        'direccion_residencia': 'Calle 10 #2-3',
        'area_desempeño': 'Matematicas'
    }
    serializer = MonitorAcademicoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    monitor = serializer.save()
    assert monitor.id is not None
    assert monitor.nombre == 'Andres'

    serializer_read = MonitorAcademicoSerializer(instance=monitor)
    assert serializer_read.data['nombre'] == 'Andres'

@pytest.mark.django_db
def test_serializador_asignacion_monitor_academico_valido(monitor_academico_instance, modulo_instance):
    data = {
        'id_monitor_academico': monitor_academico_instance.id,
        'id_modulo': modulo_instance.id_modulo
    }
    serializer = AsignacionMonitorAcademicoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_serializador_asignacion_monitor_academico_invalido():
    data = {
        'id_monitor_academico': 9999,  # No existe
        'id_modulo': 9999
    }
    serializer = AsignacionMonitorAcademicoSerializer(data=data)
    assert not serializer.is_valid()
