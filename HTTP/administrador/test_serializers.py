import pytest
from administrador.models import Administrador
from administrador.serializers import AdministradorSerializer
from cuenta.models import CustomUser

@pytest.mark.django_db
def test_serializador_administrador_valido():
    user = CustomUser.objects.create_user(username='admin_test', password='password123', user_type='administrador')
    data = {
        'user': user.id,
        'nombre': 'Carlos',
        'apellido': 'Perez',
        'correo': 'carlos.perez@example.com',
        'contrasena': 'adminpass123',
        'numero_documento': '11111111'
    }
    serializer = AdministradorSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    admin = serializer.save()
    assert admin.id_administrador is not None
    assert admin.nombre == 'Carlos'
    assert admin.user == user

    # Probar serialización (contrasena debe ser write_only, por lo que no debe estar en los datos serializados)
    serializer_read = AdministradorSerializer(instance=admin)
    assert serializer_read.data['nombre'] == 'Carlos'
    assert 'contrasena' not in serializer_read.data

@pytest.mark.django_db
def test_serializador_administrador_invalido():
    # numero_documento es obligatorio
    data = {
        'nombre': 'Carlos',
        'apellido': 'Perez',
        'correo': 'not-an-email',
        'contrasena': 'adminpass123'
    }
    serializer = AdministradorSerializer(data=data)
    assert not serializer.is_valid()
    assert 'numero_documento' in serializer.errors
    assert 'correo' in serializer.errors
