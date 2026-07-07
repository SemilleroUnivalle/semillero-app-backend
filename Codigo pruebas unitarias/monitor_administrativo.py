import pytest
from monitor_administrativo.serializers import MonitorAdministrativoSerializer
from monitor_administrativo.models import MonitorAdministrativo
from cuenta.models import CustomUser

@pytest.mark.django_db
def test_serializador_monitor_administrativo_valido():
    user = CustomUser.objects.create_user(username='mon_admin_test', password='password123', user_type='monitor_administrativo')
    data = {
        'user': user.id,
        'nombre': 'Liliana',
        'apellido': 'Cruz',
        'numero_documento': '87654321',
        'email': 'liliana@example.com',
        'ciudad_residencia': 'Cali',
        'eps': 'Sura',
        'tipo_documento': 'CC',
        'genero': 'Femenino',
        'fecha_nacimiento': '1997-03-15',
        'telefono_fijo': '3333333',
        'celular': '3201111111',
        'departamento_residencia': 'Valle',
        'comuna_residencia': '17',
        'direccion_residencia': 'Calle 10 #2-3'
    }
    serializer = MonitorAdministrativoSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    monitor = serializer.save()
    assert monitor.id is not None
    assert monitor.nombre == 'Liliana'

    serializer_read = MonitorAdministrativoSerializer(instance=monitor)
    assert serializer_read.data['nombre'] == 'Liliana'
