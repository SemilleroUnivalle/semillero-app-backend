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
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsProfesorOrAdministrador
#Transacciones atomicas
from django.db import transaction
#Serializador
from profesor.serializers import ProfesorSerializer, ProfesorModuloSerializer
from modulo.serializers import ModuloProfesorSerializer
def file_update(instance, data, field_name):
        """
        Elimina el archivo anterior y asigna el nuevo si se envía uno.
        """
        uploaded_file = data.get(field_name)
        if uploaded_file:
            # Elimina el archivo anterior de S3 si existe
            old_file = getattr(instance, field_name, None)
            if old_file:
                old_file.delete(save=False)
            setattr(instance, field_name, uploaded_file)
            instance.save()
            data.pop(field_name)

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
        
        serializer = ProfesorModuloSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Crear un profesor",
        operation_description="Crea un nuevo registro de profesor",
        responses={
            status.HTTP_201_CREATED: ProfesorSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        id_modulo = request.data.get('modulo')
        if not id_modulo:
            return Response(
                {"detail": 'El campo "modulo" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            modulo_instancia = Modulo.objects.get(id_modulo=id_modulo)
        except Modulo.DoesNotExist:
            return Response(
                {"detail": "El modulo especificado no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
                    modulo=modulo_instancia,
                    documento_identidad_pdf=request.FILES.get('documento_identidad_pdf'),
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
        try:
            data = request.data.copy() 
            instance = self.get_object()
            user = instance.user
            
            # Manejar la contraseña si está presente
            if 'contrasena' in data and data['contrasena']:
                new_password = extract_single_value(data.pop('contrasena'))
                user.set_password(new_password)
                user.save()
                hashed_password = make_password(new_password)
                instance.contrasena = hashed_password
                instance.save()
                
            #Manejar is_active
            if 'is_active' in data:
                is_active = extract_single_value(data.pop('is_active'))
                user.is_active = is_active
                user.save()
                instance.is_active = is_active
                instance.save()
            
            #Manejar el nombre de usuario
            if 'nombre' in data:
                nombre = extract_single_value(data.pop('nombre'))
                user.first_name = nombre
                user.save()
                instance.nombre = nombre
                instance.save()
                
            #Manejar el apellido
            if 'apellido' in data:
                apellido = extract_single_value(data.pop('apellido'))
                user.last_name = apellido
                user.save()
                instance.apellido = apellido
                instance.save()
            
            #Manejar el email
            if 'email' in data:
                email = extract_single_value(data.pop('email'))
                user.email = email
                user.save()
                instance.email = email
                instance.save()
            
            file_update(instance, data, 'documento_identidad_pdf')

            if data:
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                # Si solo se cambió la contraseña y no hay otros campos, devolvemos los datos actualizados
                serializer = self.get_serializer(instance)
                return Response(serializer.data)

        except TypeError as e:
            # Este error ocurre si intentas copiar archivos grandes
            return Response(
                {"detail": "Error procesando archivos grandes", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Cubre cualquier otro error inesperado
            return Response(
                {"detail": "Ocurrió un error inesperado.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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
                serializer_profesor = ProfesorSerializer(profesor)
                modulo = Modulo.objects.get(id_modulo=modulo_id)
                serializer_modulo = ModuloProfesorSerializer(modulo)
                
                # Si el profesor ya tenía un módulo asignado, mostramos mensaje informativo
                mensaje = "Asignación realizada correctamente"
                if profesor.modulo:
                    mensaje = f"El profesor estaba asignado al módulo {profesor.modulo.nombre_modulo}. Se ha actualizado la asignación."
                
                profesor.modulo = modulo
                profesor.save()
                
                return Response({
                    "mensaje": mensaje,
                    "profesor": serializer_profesor.data,
                    "modulo": serializer_modulo.data,
                }, status=status.HTTP_200_OK)
                
            except Profesor.DoesNotExist:
                return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Modulo.DoesNotExist:
                return Response({"error": "Módulo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
