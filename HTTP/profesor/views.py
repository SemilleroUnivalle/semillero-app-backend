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
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsProfesorOrAdministrador, IsSelfOrAdmin
#Transacciones atomicas
from django.db import transaction
#Serializador
from .serializers import ProfesorSerializer, AsignacionProfesorSerializer, ProfesorModuloSerializer
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
def extract_single_value(value):
        if isinstance(value, list):
            return value[0] if value else ''
        return value
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
            permission_classes = [IsSelfOrAdmin]
        else: 
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Profesores",
        operation_description="Retorna una lista de todos los profesores, registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = ProfesorModuloSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Crear un profesor",
        responses={
            status.HTTP_201_CREATED: ProfesorSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        id_modulo = request.data.get('modulo')
        if not id_modulo:
            modulo_instancia = None
        else:
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
                profesor = Profesor.objects.create(
                    user=user,
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    contrasena=hashed_password,
                    numero_documento=data.get('numero_documento'),
                    email=data.get('email'),
                    ciudad_residencia=data.get('ciudad_residencia'),
                    eps=data.get('eps'),
                    tipo_documento=data.get('tipo_documento'),
                    genero=data.get('genero'),
                    fecha_nacimiento=data.get('fecha_nacimiento'),
                    telefono_fijo=data.get('telefono_fijo'),
                    celular=data.get('celular'),
                    departamento_residencia=data.get('departamento_residencia'),
                    comuna_residencia=data.get('comuna_residencia'),
                    direccion_residencia=data.get('direccion_residencia'),
                    documento_identidad_pdf=request.FILES.get('documento_identidad_pdf'),
                    rut_pdf=request.FILES.get('rut_pdf'),
                    certificado_bancario_pdf=request.FILES.get('certificado_bancario_pdf'),
                    area_desempeño=data.get('area_desempeño', ''),
                    grado_escolaridad=data.get('grado_escolaridad', ''),
                    hoja_vida_pdf=request.FILES.get('hoja_vida_pdf'),
                    certificado_laboral_pdf=request.FILES.get('certificado_laboral_pdf'),
                    certificado_academico_pdf=request.FILES.get('certificado_academico_pdf'),
                    modulo=modulo_instancia,
                    
                )
                # Puedes retornar la información deseada
            return Response({'id': profesor.id}, status=status.HTTP_201_CREATED)
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

            pdf_fields = [
                'documento_identidad_pdf',
                'rut_pdf',
                'certificado_bancario_pdf',
                'hoja_vida_pdf',
                'certificado_laboral_pdf',
                'certificado_academico_pdf',
            ]

            numero_documento_actualizado = False
            nuevo_numero_documento = None
            
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

            if 'numero_documento' in data:
                numero_documento = extract_single_value(data.pop('numero_documento'))
                user.username = numero_documento
                user.save()
                instance.numero_documento = numero_documento
                instance.save()
                numero_documento_actualizado = True
                nuevo_numero_documento = numero_documento

            # Actualización de nombre de archivos PDF si numero_documento fue actualizado
            if numero_documento_actualizado:
                for field in pdf_fields:
                    file_field = getattr(instance, field, None)
                    if file_field and hasattr(file_field, 'name') and file_field.name:
                        import os
                        from django.core.files.base import ContentFile

                        old_file_name = file_field.name  # Ruta completa en el bucket
                        file_content = file_field.read()  # Lee el contenido antes de borrar

                        # Elimina el archivo viejo del bucket
                        storage = file_field.storage
                        if storage.exists(old_file_name):
                            storage.delete(old_file_name)

                        # Construye el nuevo nombre
                        new_filename = f"{nuevo_numero_documento}.pdf"
                        file_dir = os.path.dirname(old_file_name)
                        new_file_path = os.path.join(file_dir, new_filename)

                        # Sube el archivo con el nuevo nombre
                        getattr(instance, field).save(new_file_path, ContentFile(file_content), save=True)
            
            file_update(instance, data, 'documento_identidad_pdf')
            file_update(instance, data, 'rut_pdf')
            file_update(instance, data, 'certificado_bancario_pdf')
            file_update(instance, data, 'hoja_vida_pdf')
            file_update(instance, data, 'certificado_laboral_pdf')
            file_update(instance, data, 'certificado_academico_pdf')

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
