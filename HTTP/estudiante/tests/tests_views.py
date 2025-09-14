import pytest
import os
from unittest.mock import patch, MagicMock
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from ..views import EstudianteViewSet
from ..models import Estudiante
from cuenta.models import CustomUser

CustomUser = get_user_model()

@pytest.fixture
def configurar_estudiante():
    # Crear usuario administrador
    admin = CustomUser.objects.create_user(
        username='admin_test',
        password='adminpass123',
        user_type='administrador',
        is_superuser=False,
        is_staff=True
    )
    
    # Crear usuario regular
    usuario_regular = CustomUser.objects.create_user(
        username='regular_test',
        password='userpass123',
        user_type='profesor'
    )
    
    # Crear usuario estudiante
    usuario_estudiante = CustomUser.objects.create_user(
        username='12345678',
        password='estudpass123',
        user_type='estudiante',
        first_name='Test',
        last_name='Student'
    )
    
    # Crear perfil de estudiante
    estudiante = Estudiante.objects.create(
        user=usuario_estudiante,
        numero_documento='12345678',
        contrasena=usuario_estudiante.password,
        nombre='Test',
        apellido='Student',
        email='test@example.com',
        is_active=True
    )
    
    # Crear token para el estudiante
    token = Token.objects.create(user=usuario_estudiante)
    
    return {
        'admin': admin,
        'usuario_regular': usuario_regular,
        'usuario_estudiante': usuario_estudiante,
        'estudiante': estudiante,
        'token': token
    }

@pytest.mark.django_db
class TestEstudianteViewSetEliminar:
    
    def test_permiso_eliminar_admin_permitido(self, configurar_estudiante):
        """Prueba que los administradores pueden eliminar estudiantes"""
        admin = configurar_estudiante['admin']
        estudiante = configurar_estudiante['estudiante']
        
        factory = APIRequestFactory()
        vista = EstudianteViewSet.as_view({'delete': 'destroy'})
        
        # Hacer petición como administrador
        peticion = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(peticion, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_cliente_s3:
            mock_client = MagicMock()
            mock_cliente_s3.return_value = mock_client
            
            respuesta = vista(peticion, pk=estudiante.id_estudiante)
            
            assert respuesta.status_code == status.HTTP_204_NO_CONTENT
            assert 'Estudiante y archivos eliminados correctamente' in respuesta.data['detail']
            assert not Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()
    
    def test_permiso_eliminar_denegado_para_usuario_regular(self, configurar_estudiante):
        """Prueba que los usuarios no administradores no pueden eliminar estudiantes"""
        usuario_regular = configurar_estudiante['usuario_regular']
        estudiante = configurar_estudiante['estudiante']
        
        factory = APIRequestFactory()
        vista = EstudianteViewSet.as_view({'delete': 'destroy'})
        
        # Hacer petición como usuario regular
        peticion = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(peticion, user=usuario_regular)
        
        respuesta = vista(peticion, pk=estudiante.id_estudiante)
        
        assert respuesta.status_code == status.HTTP_403_FORBIDDEN
        assert Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()
    
    def test_eliminar_archivos_s3(self, configurar_estudiante):
        """Prueba que el método eliminar intenta borrar los archivos asociados en S3"""
        admin = configurar_estudiante['admin']
        estudiante = configurar_estudiante['estudiante']
        
        # Configurar archivos simulados con nombres
        estudiante.documento_identidad = MagicMock()
        estudiante.documento_identidad.name = 'test_document.pdf'
        estudiante.foto = MagicMock()
        estudiante.foto.name = 'test_photo.jpg'
        estudiante.save()
        
        factory = APIRequestFactory()
        vista = EstudianteViewSet.as_view({'delete': 'destroy'})
        peticion = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(peticion, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_cliente_s3:
            mock_client = MagicMock()
            mock_cliente_s3.return_value = mock_client
            
            respuesta = vista(peticion, pk=estudiante.id_estudiante)
            
            # Verificar que el cliente S3 fue llamado para eliminar archivos
            assert mock_client.delete_object.call_count == 2  # Dos archivos con nombres
            # Verificar que se usaron las claves correctas
            claves_esperadas = [
                f"media/{estudiante.documento_identidad.name.lstrip('/')}",
                f"media/{estudiante.foto.name.lstrip('/')}"
            ]
            claves_reales = [
                call[1]['Key'] for call in mock_client.delete_object.call_args_list
            ]
            for clave in claves_esperadas:
                assert clave in claves_reales
    
    def test_eliminar_usuario_y_token(self, configurar_estudiante):
        """Prueba que el método eliminar también borra el usuario asociado y su token"""
        admin = configurar_estudiante['admin']
        estudiante = configurar_estudiante['estudiante']
        usuario_estudiante = configurar_estudiante['usuario_estudiante']
        token = configurar_estudiante['token']
        id_usuario = usuario_estudiante.id
        
        # Verificar que el usuario y token existen
        assert CustomUser.objects.filter(id=id_usuario).exists()
        assert Token.objects.filter(user=usuario_estudiante).exists()
        
        factory = APIRequestFactory()
        vista = EstudianteViewSet.as_view({'delete': 'destroy'})
        peticion = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(peticion, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_cliente_s3:
            mock_cliente_s3.return_value = MagicMock()
            respuesta = vista(peticion, pk=estudiante.id_estudiante)
            
            # Verificar que el usuario y token fueron eliminados
            assert not CustomUser.objects.filter(id=id_usuario).exists()
            assert not Token.objects.filter(user_id=id_usuario).exists()
    
    def test_manejo_excepciones_eliminar(self, configurar_estudiante):
        """Prueba que el método eliminar maneja las excepciones al borrar archivos S3 correctamente"""
        admin = configurar_estudiante['admin']
        estudiante = configurar_estudiante['estudiante']
        
        # Configurar archivo con nombre
        estudiante.documento_identidad = MagicMock()
        estudiante.documento_identidad.name = 'test_doc.pdf'
        estudiante.save()
        
        factory = APIRequestFactory()
        vista = EstudianteViewSet.as_view({'delete': 'destroy'})
        peticion = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(peticion, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_cliente_s3:
            # Simular que el cliente S3 lanza una excepción al eliminar
            mock_client = MagicMock()
            mock_client.delete_object.side_effect = Exception("Error al borrar en S3")
            mock_cliente_s3.return_value = mock_client
            
            # La vista debería seguir teniendo éxito aunque falle la eliminación en S3
            respuesta = vista(peticion, pk=estudiante.id_estudiante)
            
            assert respuesta.status_code == status.HTTP_204_NO_CONTENT
            assert not Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()