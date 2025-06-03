from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Profesor
from cuenta.models import CustomUser
#Serializadores
from .serializers import ProfesorSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsProfesorOrAdministrador


class ProfesorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar Profesores.
    
    Permite listar, crear, actualizar y eliminar profesores.
    """
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'retrive']:
            permission_classes = [IsProfesorOrAdministrador]
        else: 
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Profesores",
        operation_description="Retorna una lista de todos los Profesores, registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un profesor",
        operation_description="Crea un nuevo registro de profesor",
        responses={
            status.HTTP_201_CREATED: ProfesorSerializer,
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
        
        # Crear el usuario
        user = CustomUser.objects.create(
            username=data.get('numero_documento'),
            password=hashed_password,
            user_type='profesor',
            first_name=data.get('nombre'),
            last_name=data.get('apellido'),
            email=data.get('correo'),
            is_active=True,
            is_staff=True,
            is_superuser=False,
        )
        
        # Crear el perfil de profesor
        Profesor.objects.create(
            user=user,
            numero_documento=data.get('numero_documento'),
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            correo=data.get('correo'),
            telefono=data.get('telefono'),
            contrasena=hashed_password,
            fecha_nacimiento=data.get('fecha_nacimiento'),
            fecha_contratacion=data.get('fecha_contratacion'),
            salario=data.get('salario'),
            
        )

        # Puedes retornar la información deseada
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener un profesor específico",
        operation_description="Retorna los detalles de un profesor específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un profesor",
        operation_description="Actualiza todos los campos de un profesor existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        
        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos del profesor actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un profesor",
        operation_description="Actualiza uno o más campos de un profesor existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un profesor",
        operation_description="Elimina permanentemente un profesor del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        user = None
        
        try:
            user = instance.user
        except Exception:
            pass
        
        self.perform_destroy(instance)
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
