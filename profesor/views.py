from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Profesor
from cuenta.models import CustomUser
from modulo.models import Modulo
from .serializers import ProfesorSerializer, AsignacionProfesorSerializer
#Serializadores
from .serializers import ProfesorSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsProfesorOrAdministrador
#Transacciones atomicas
from django.db import transaction

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
        
        try:
            with transaction.atomic():
                # Crear el usuario
                user = CustomUser.objects.create(
                    username=data.get('numero_documento'),
                    password=hashed_password,
                    user_type='profesor',
                    first_name=data.get('nombre'),
                    last_name=data.get('apellido'),
                    email=data.get('email'),
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
                    email=data.get('email'),
                    celular=data.get('celular'),
                    contrasena=hashed_password,
                    area_desempeño=data.get('area_desempeño', ''),
                    grado_escolaridad=data.get('grado_escolaridad', ''),
                    modulo=data.get('modulo', None)
                )
                # Puedes retornar la información deseada
            return Response({'detail': 'Profesor creado exitosamente'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Error al crear profesor: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

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
    
    @swagger_auto_schema(
        operation_summary="Asignar un módulo a un profesor",
        operation_description="Asigna un módulo específico a un profesor. Si el profesor ya tenía un módulo asignado, se actualiza la asignación.",
        request_body=AsignacionProfesorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Asignación exitosa",
                examples={
                    "application/json": {
                        "mensaje": "Asignación realizada correctamente",
                        "profesor": {
                            "id": 1,
                            "nombre": "Juan Pérez"
                        },
                        "modulo": {
                            "id": 2,
                            "nombre": "Matemáticas"
                        }
                    }
                }
            ),
            status.HTTP_404_NOT_FOUND: "Profesor o módulo no encontrado",
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    @action(detail=False, methods=['post'])
    def asignar_modulo(self, request):
        serializer = AsignacionProfesorSerializer(data=request.data)
        
        if serializer.is_valid():
            profesor_id = serializer.validated_data['id_profesor']
            modulo_id = serializer.validated_data['id_modulo']
            
            try:
                profesor = Profesor.objects.get(id_profesor=profesor_id)
                modulo = Modulo.objects.get(id_modulo=modulo_id)
                
                # Si el profesor ya tenía un módulo asignado, mostramos mensaje informativo
                mensaje = "Asignación realizada correctamente"
                if profesor.modulo:
                    mensaje = f"El profesor estaba asignado al módulo {profesor.modulo.nombre_modulo}. Se ha actualizado la asignación."
                
                profesor.modulo = modulo
                profesor.save()
                
                return Response({
                    "mensaje": mensaje,
                    "profesor": {
                        "id": profesor.id_profesor,
                        "nombre": f"{profesor.nombre} {profesor.apellido}"
                    },
                    "modulo": {
                        "id": modulo.id_modulo,
                        "nombre": modulo.nombre_modulo
                    }
                }, status=status.HTTP_200_OK)
                
            except Profesor.DoesNotExist:
                return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Modulo.DoesNotExist:
                return Response({"error": "Módulo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
