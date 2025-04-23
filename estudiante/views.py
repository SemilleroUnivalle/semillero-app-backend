from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Estudiante
from cuenta.models import CustomUser
#Serializadores
from .serializers import EstudianteSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class EstudianteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar estudiantes.
    
    Permite listar, crear, actualizar y eliminar estudiantes.
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    
    permission_classes = [IsAuthenticated]  
    
    def get_permissions(self):
        """
        Define permisos según la acción solicitada:
        - list: Profesores y administradores pueden ver todos los estudiantes
        - retrieve, update, partial_update: Estudiantes pueden ver/actualizar sus propios datos, administradores pueden todos
        - create, destroy: Solo administradores
        """
        if self.action == 'list':
            # Profesores y administradores pueden listar
            permission_classes = [IsProfesorOrAdministrador]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Estudiantes pueden ver/editar su perfil, administradores pueden todos
            # La restricción de que el estudiante solo vea su perfil se controla en retrieve
            permission_classes = [IsEstudiante | IsAdministrador]
        elif self.action in ['create', 'destroy']:
            # Solo administradores pueden crear/eliminar
            permission_classes = [IsAdministrador]
        else:
            # Para cualquier otra acción, usuario autenticado
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    # Modificar retrieve para que estudiante solo vea su propio perfil
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Si es estudiante, solo puede ver su propio perfil
        if request.user.user_type == 'estudiante' and (
            not hasattr(request.user, 'estudiante') or 
            request.user.estudiante.id_estudiante != instance.id_estudiante
        ):
            return Response(
                {"detail": "No tienes permiso para ver este perfil"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Listar todos los estudiantes",
        operation_description="Retorna una lista de todos los estudiantes registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando estudiantes")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un estudiante",
        operation_description="Crea un nuevo registro de estudiante",
        responses={
            status.HTTP_201_CREATED: EstudianteSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        # Verificar si el usuario ya existe
        username = data.get('numero_documento', '')
        if CustomUser.objects.filter(username=username).exists():
            return Response({'detail': 'El numero de identificacion ya esta registrado'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no se proporciona contraseña, usa el número de documento
        if not data.get('contrasena'):
            data['contrasena'] = data.get('numero_documento', '')
        
        # Hashear la contraseña
        hashed_password = make_password(data['contrasena'])
        
        # Crear el usuario
        user = CustomUser.objects.create(
            username=data.get('numero_documento'),
            password=hashed_password,
            user_type='estudiante',
            first_name=data.get('nombre'),
            last_name=data.get('apellido'),
            email=data.get('email'),
            is_superuser=False,
            is_staff=False,
            is_active=data.get('is_active', True),
        )
        
        # Crear el perfil de estudiante
        Estudiante.objects.create(
            user=user,
            numero_documento=data.get('numero_documento'),
            contrasena=hashed_password,
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            email=data.get('email'),
            is_active=data.get('is_active'),
            acudiente=data.get('acudiente'),
            registro_fase=data.get('registro_fase'),
            ciudad_residencia=data.get('ciudad_residencia'),
            ciudad_documento=data.get('ciudad_documento'),
            id_eps=data.get('id_eps'),
            id_grado=data.get('id_grado'),
            tipo_documento=data.get('tipo_documento'),
            genero=data.get('genero'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            telefono_fijo=data.get('telefono_fijo'),
            celular=data.get('celular'),
            departamento_residencia=data.get('departamento_residencia'),
            comuna_residencia=data.get('comuna_residencia'),
            direccion_residencia=data.get('direccion_residencia'),
            estamento=data.get('estamento'),
            discapacidad=data.get('discapacidad'),
            tipo_discapacidad=data.get('tipo_discapacidad'),
            descripcion_discapacidad=data.get('descripcion_discapacidad')
        )

        # Puedes retornar la información deseada
        return Response({'detail': 'Estudiante creado exitosamente'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener un estudiante específico",
        operation_description="Retorna los detalles de un estudiante específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un estudiante",
        operation_description="Actualiza todos los campos de un estudiante existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizando estudiante con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Estudiante actualizado exitosamente")

        #Responder con los datos del estudiante actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un estudiante",
        operation_description="Actualiza uno o más campos de un estudiante existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un estudiante",
        operation_description="Elimina permanentemente un estudiante del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
