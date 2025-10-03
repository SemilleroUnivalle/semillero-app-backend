from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import MonitorAdministrativo
from cuenta.models import CustomUser
#Serializadores
from .serializers import MonitorAdministrativoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsSelfOrAdmin
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
#Transacciones atomicas
from django.db import transaction
#Auditoria
from auditlog.models import LogEntry
from .serializers import LogEntrySerializer
from auditlog.context import set_actor
from django.contrib.contenttypes.models import ContentType

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

class MonitorAdministrativoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar administradores.
    
    Permite listar, crear, actualizar y eliminar adminisradores.
    Solo los usuarios administradores tienen acceso a estas operaciones.
    """
    queryset = MonitorAdministrativo.objects.all()
    serializer_class = MonitorAdministrativoSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsSelfOrAdmin]
        else: 
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
        
    
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
            status.HTTP_201_CREATED: MonitorAdministrativoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

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
                # Crear el usuario sin contraseña y asignarla usando set_password
                user = CustomUser.objects.create(
                    username=data.get('numero_documento'),
                    password=hashed_password,
                    first_name=data.get('nombre'),
                    last_name=data.get('apellido'),
                    email=data.get('email'),
                    user_type='monitor_administrativo',
                    is_superuser=True,
                    is_active=True,
                    is_staff=True,
                )
            

                # Crear el perfil de administrador
                monitor_administrativo = MonitorAdministrativo.objects.create(
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
                    d10_pdf=request.FILES.get('d10_pdf'),
                    tabulado_pdf=request.FILES.get('tabulado_pdf'),
                    estado_mat_financiera_pdf=request.FILES.get('estado_mat_financiera_pdf'),
                )
                # Puedes retornar la información deseada
            return Response({'id': monitor_administrativo.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Error al crear Monitor academico: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Obtener un Monitor administrativo específico",
        operation_description="Retorna los detalles de un Monitor administrativo específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un Monitor administrativo",
        operation_description="Actualiza todos los campos de un Monitor administrativo existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un Monitor administrativo",
        operation_description="Actualiza uno o más campos de un Monitor administrativo existente"
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
                'd10_pdf',
                'tabulado_pdf',
                'estado_mat_financiera_pdf',
            ]

            numero_documento_actualizado = False
            nuevo_numero_documento = None

            with set_actor(request.user):
                # Manejar la contraseña si está presente
                if 'contrasena' in data and data['contrasena']:
                    new_password = extract_single_value(data.pop('contrasena'))
                    user.set_password(new_password)
                    user.save()
                    hashed_password = make_password(new_password)
                    instance.contrasena = hashed_password
                    instance.save()

                # Manejar is_active
                if 'is_active' in data:
                    is_active = extract_single_value(data.pop('is_active'))
                    user.is_active = is_active
                    user.save()
                    instance.is_active = is_active
                    instance.save()

                # Manejar el nombre de usuario
                if 'nombre' in data:
                    nombre = extract_single_value(data.pop('nombre'))
                    user.first_name = nombre
                    user.save()
                    instance.nombre = nombre
                    instance.save()

                # Manejar el apellido
                if 'apellido' in data:
                    apellido = extract_single_value(data.pop('apellido'))
                    user.last_name = apellido
                    user.save()
                    instance.apellido = apellido
                    instance.save()

                # Manejar el email
                if 'email' in data:
                    email = extract_single_value(data.pop('email'))
                    user.email = email
                    user.save()
                    instance.email = email
                    instance.save()

                # Manejar numero_documento
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

                # Actualización normal de archivos si no hay cambio de nombre
                file_update(instance, data, 'documento_identidad_pdf')
                file_update(instance, data, 'rut_pdf')
                file_update(instance, data, 'certificado_bancario_pdf')
                file_update(instance, data, 'd10_pdf')
                file_update(instance, data, 'tabulado_pdf')
                file_update(instance, data, 'estado_mat_financiera_pdf')

                if data:
                    serializer = self.get_serializer(instance, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    return Response(serializer.data)
                else:
                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

        except Exception as e:
            return Response(
                {"detail": "Ocurrió un error inesperado.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Utilizo perform_update para actualizar el estado del monitor administrativo a (No revisado, Revisado, Pendiente)
    def perform_update(self, serializer):
        instance = serializer.instance  # aún no ha guardado los cambios

        # Guarda valores originales
        d10_original = instance.verificacion_d10
        tabulado_original = instance.verificacion_tabulado
        estado_mat_financiera_original = instance.verificacion_estado_mat_financiera
        documento_identidad_original = instance.verificacion_documento_identidad
        rut_original = instance.verificacion_rut
        certificado_bancario_original = instance.verificacion_certificado_bancario
        foto_original = instance.verificacion_foto
        informacion_original = instance.verificacion_informacion

        # Guarda cambios nuevos
        instance = serializer.save()
        d10_nuevo = instance.verificacion_d10
        tabulado_nuevo = instance.verificacion_tabulado
        estado_mat_financiera_nuevo = instance.verificacion_estado_mat_financiera
        documento_identidad_nuevo = instance.verificacion_documento_identidad
        rut_nuevo = instance.verificacion_rut
        certificado_bancario_nuevo = instance.verificacion_certificado_bancario
        foto_nuevo = instance.verificacion_foto
        informacion_nuevo = instance.verificacion_informacion

        # Asigna el estado correcto
        if d10_nuevo and tabulado_nuevo and estado_mat_financiera_nuevo and documento_identidad_nuevo and rut_nuevo and certificado_bancario_nuevoand and foto_nuevo and informacion_nuevo:
            instance.estado = "Revisado"
        elif d10_nuevo or tabulado_nuevo or estado_mat_financiera_nuevo or documento_identidad_nuevo or rut_nuevo or certificado_bancario_nuevo or foto_nuevo or informacion_nuevo:
            instance.estado = "Pendiente"
        else:
            instance.estado = "No revisado"

        instance.save(update_fields=['estado'])

        # Busca el último logentry después de guardar
        content_type = ContentType.objects.get_for_model(instance)
        logentry = LogEntry.objects.filter(
            object_id=instance.pk,
            content_type=content_type
        ).order_by('-timestamp').first()


        # Solo actualiza el campo de auditoría si el valor fue cambiado
        if d10_original != d10_nuevo and logentry:
            instance.audit_d10 = logentry
        if tabulado_original != tabulado_nuevo and logentry:
            instance.audit_tabulado = logentry
        if estado_mat_financiera_original != estado_mat_financiera_nuevo and logentry:
            instance.audit_estado_mat_financiera = logentry
        if documento_identidad_original != documento_identidad_nuevo and logentry:
            instance.audit_documento_identidad = logentry
        if rut_original != rut_nuevo and logentry:
            instance.audit_rut = logentry
        if certificado_bancario_original != certificado_bancario_nuevo and logentry:
            instance.audit_certificado_bancario = logentry
        if foto_original != foto_nuevo and logentry:
            instance.audit_foto = logentry
        if informacion_original != informacion_nuevo and logentry:
            instance.audit_informacion = logentry

        # Guarda solo los campos que hayan cambiado
        campos_actualizados = []
        if d10_original != d10_nuevo:
            campos_actualizados.append('audit_d10')
        if tabulado_original != tabulado_nuevo:
            campos_actualizados.append('audit_tabulado')
        if estado_mat_financiera_original != estado_mat_financiera_nuevo:
            campos_actualizados.append('audit_estado_mat_financiera')
        if documento_identidad_original != documento_identidad_nuevo:
            campos_actualizados.append('audit_documento_identidad')
        if rut_original != rut_nuevo:
            campos_actualizados.append('audit_rut')
        if certificado_bancario_original != certificado_bancario_nuevo:
            campos_actualizados.append('audit_certificado_bancario')
        if foto_original != foto_nuevo:
            campos_actualizados.append('audit_foto')
        if informacion_original != informacion_nuevo:
            campos_actualizados.append('audit_informacion')

        if campos_actualizados:
            instance.save(update_fields=campos_actualizados)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un Monitor administrativo",
        operation_description="Elimina permanentemente un Monitor administrativo del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)