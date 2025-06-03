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
def setup_estudiante():
    # Create admin user
    admin = CustomUser.objects.create_user(
        username='admin_test',
        password='adminpass123',
        user_type='administrador',
        is_superuser=False,
        is_staff=True
    )
    
    # Create regular user
    regular_user = CustomUser.objects.create_user(
        username='regular_test',
        password='userpass123',
        user_type='profesor'
    )
    
    # Create estudiante user
    estudiante_user = CustomUser.objects.create_user(
        username='12345678',
        password='estudpass123',
        user_type='estudiante',
        first_name='Test',
        last_name='Student'
    )
    
    # Create estudiante profile
    estudiante = Estudiante.objects.create(
        user=estudiante_user,
        numero_documento='12345678',
        contrasena=estudiante_user.password,
        nombre='Test',
        apellido='Student',
        email='test@example.com',
        is_active=True
    )
    
    # Create token for estudiante
    token = Token.objects.create(user=estudiante_user)
    
    return {
        'admin': admin,
        'regular_user': regular_user,
        'estudiante_user': estudiante_user,
        'estudiante': estudiante,
        'token': token
    }

@pytest.mark.django_db
class TestEstudianteViewSetDestroy:
    
    def test_destroy_permission_admin_allowed(self, setup_estudiante):
        """Test that administrators can delete students"""
        admin = setup_estudiante['admin']
        estudiante = setup_estudiante['estudiante']
        
        factory = APIRequestFactory()
        view = EstudianteViewSet.as_view({'delete': 'destroy'})
        
        # Make request as admin
        request = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(request, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_s3_client:
            mock_client = MagicMock()
            mock_s3_client.return_value = mock_client
            
            response = view(request, pk=estudiante.id_estudiante)
            
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert 'Estudiante y archivos eliminados correctamente' in response.data['detail']
            assert not Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()
    
    def test_destroy_permission_denied_for_regular_user(self, setup_estudiante):
        """Test that non-admin users cannot delete students"""
        regular_user = setup_estudiante['regular_user']
        estudiante = setup_estudiante['estudiante']
        
        factory = APIRequestFactory()
        view = EstudianteViewSet.as_view({'delete': 'destroy'})
        
        # Make request as regular user
        request = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(request, user=regular_user)
        
        response = view(request, pk=estudiante.id_estudiante)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()
    
    def test_destroy_deletes_s3_files(self, setup_estudiante):
        """Test that destroy method attempts to delete associated S3 files"""
        admin = setup_estudiante['admin']
        estudiante = setup_estudiante['estudiante']
        
        # Set up mock files with names
        estudiante.documento_identidad = MagicMock()
        estudiante.documento_identidad.name = 'test_document.pdf'
        estudiante.foto = MagicMock()
        estudiante.foto.name = 'test_photo.jpg'
        estudiante.save()
        
        factory = APIRequestFactory()
        view = EstudianteViewSet.as_view({'delete': 'destroy'})
        request = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(request, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_s3_client:
            mock_client = MagicMock()
            mock_s3_client.return_value = mock_client
            
            response = view(request, pk=estudiante.id_estudiante)
            
            # Assert S3 client was called to delete files
            assert mock_client.delete_object.call_count == 2  # Two files with names
            # Check that the right keys were used
            expected_keys = [
                f"media/{estudiante.documento_identidad.name.lstrip('/')}",
                f"media/{estudiante.foto.name.lstrip('/')}"
            ]
            actual_keys = [
                call[1]['Key'] for call in mock_client.delete_object.call_args_list
            ]
            for key in expected_keys:
                assert key in actual_keys
    
    def test_destroy_deletes_user_and_token(self, setup_estudiante):
        """Test that destroy method also deletes associated user and token"""
        admin = setup_estudiante['admin']
        estudiante = setup_estudiante['estudiante']
        estudiante_user = setup_estudiante['estudiante_user']
        token = setup_estudiante['token']
        user_id = estudiante_user.id
        
        # Verify user and token exist
        assert CustomUser.objects.filter(id=user_id).exists()
        assert Token.objects.filter(user=estudiante_user).exists()
        
        factory = APIRequestFactory()
        view = EstudianteViewSet.as_view({'delete': 'destroy'})
        request = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(request, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_s3_client:
            mock_s3_client.return_value = MagicMock()
            response = view(request, pk=estudiante.id_estudiante)
            
            # Verify that user and token are deleted
            assert not CustomUser.objects.filter(id=user_id).exists()
            assert not Token.objects.filter(user_id=user_id).exists()
    
    def test_destroy_handles_exceptions_gracefully(self, setup_estudiante):
        """Test that the destroy method handles exceptions when deleting S3 files"""
        admin = setup_estudiante['admin']
        estudiante = setup_estudiante['estudiante']
        
        # Set up file with name
        estudiante.documento_identidad = MagicMock()
        estudiante.documento_identidad.name = 'test_doc.pdf'
        estudiante.save()
        
        factory = APIRequestFactory()
        view = EstudianteViewSet.as_view({'delete': 'destroy'})
        request = factory.delete(f'/api/estudiantes/{estudiante.id_estudiante}/')
        force_authenticate(request, user=admin)
        
        with patch('estudiante.views.EstudianteViewSet.get_s3_client') as mock_s3_client:
            # Simulate S3 client throwing an exception when deleting
            mock_client = MagicMock()
            mock_client.delete_object.side_effect = Exception("S3 delete failed")
            mock_s3_client.return_value = mock_client
            
            # The view should still succeed even if S3 deletion fails
            response = view(request, pk=estudiante.id_estudiante)
            
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert not Estudiante.objects.filter(id_estudiante=estudiante.id_estudiante).exists()