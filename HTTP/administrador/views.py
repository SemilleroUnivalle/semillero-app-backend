from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Administrador
from cuenta.models import CustomUser
#Serializadores
from .serializers import AdministradorSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class AdministradorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar administradores.
    
    Permite listar, crear, actualizar y eliminar adminisradores.
    Solo los usuarios administradores tienen acceso a estas operaciones.
    """
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    
    #permission_classes = [IsAuthenticated, IsAdministrador]
    """
    def get_permissions(self):
        
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
        """
    
    @swagger_auto_schema(
        operation_summary="Listar todos los administradores",
        operation_description="Retorna una lista de todos los administradores, registrados"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un administrador",
        operation_description="Crea un nuevo registro de administrador",
        responses={
            status.HTTP_201_CREATED: AdministradorSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        # Verificar si el usuario ya existe
        username = data.get('numero_documento', '')
        if CustomUser.objects.filter(username=username).exists():
            return Response({'detail': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no se proporciona contraseña, usa el número de documento
        if not data.get('contrasena'):
            data['contrasena'] = data.get('numero_documento', '')

        # Hashear la contraseña
        hashed_password = make_password(data['contrasena'])

        # Crear el usuario sin contraseña y asignarla usando set_password
        user = CustomUser.objects.create(
            username=data.get('numero_documento'),
            password=hashed_password,
            first_name=data.get('nombre'),
            last_name=data.get('apellido'),
            email=data.get('correo'),
            user_type='administrador',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )
    

        # Crear el perfil de administrador
        Administrador.objects.create(
            user=user,
            numero_documento=data.get('numero_documento'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            correo=data.get('correo'),
            contrasena=hashed_password,
            fecha_creacion=data.get('fecha_creacion'),
            fecha_modificacion=data.get('fecha_modificacion'),
        )

        return Response({'detail': 'Administrador creado exitosamente'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener un administrador específico",
        operation_description="Retorna los detalles de un administrador específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un administrador",
        operation_description="Actualiza todos los campos de un administrador existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos del administrador actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un administrador",
        operation_description="Actualiza uno o más campos de un administrador existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un administrador",
        operation_description="Elimina permanentemente un administrador del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        user = None
        
        try:
            user = instance.user
        except Exception:
            pass
        
        if user:
            try:
                # Primero eliminar tokens asociados si los hay
                from rest_framework.authtoken.models import Token
                Token.objects.filter(user=user).delete()
                # Luego eliminar el usuario
                user.delete()
            except Exception as e:
                # Log the error but don't interrupt the response
                print(f"Error eliminando usuario: {str(e)}")
        return super().destroy(request, *args, **kwargs)
