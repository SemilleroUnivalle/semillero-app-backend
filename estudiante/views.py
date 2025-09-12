import os
from dotenv import load_dotenv
load_dotenv()
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Estudiante
from cuenta.models import CustomUser
from acudiente.models import Acudiente
#Serializadores
from .serializers import EstudianteSerializer, LoteEliminarSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador, IsEstudianteOrProfesor, IsEstudianteOrAdministrador
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
#Transacciones atomicas
from django.db import transaction
#HTTP
from django.http import HttpResponse
from rest_framework.response import Response
#fecha y hora 
from datetime import datetime
#Amazon S3
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
#Acciones
from rest_framework.decorators import action
#pandas
import pandas as pd
#filtros
from django_filters.rest_framework import DjangoFilterBackend

class EstudianteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar estudiantes.
    
    Permite listar, crear, actualizar y eliminar estudiantes.
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
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
            permission_classes = [IsEstudianteOrAdministrador]
        elif self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['destroy']:
            # Solo administradores pueden crear/eliminar
            permission_classes = [IsAdministrador]
        else:
            # Para cualquier otra acción, usuario autenticado
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    # Modificar retrieve para que estudiante solo vea su propio perfil
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if getattr(user, 'user_type', None) == 'estudiante':
            estudiante_rel = getattr(user, 'estudiante', None)
            if not estudiante_rel or estudiante_rel.id_estudiante != instance.id_estudiante:
                return Response(
                    {"detail": "No tienes permiso para ver este perfil"},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Acción "me"
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        if getattr(request.user, 'user_type', None) != 'estudiante':
            return Response({'detail': 'El usuario autenticado no es estudiante'}, status=status.HTTP_403_FORBIDDEN)
        # Asumiendo relación OneToOne user.estudiante
        est = request.user.estudiante
        serializer = self.get_serializer(est)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Listar todos los estudiantes",
        operation_description="Retorna una lista de todos los estudiantes registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
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
        data = request.data.copy()
        id_acudiente = request.data.get('acudiente')
        if not id_acudiente:
            return Response(
                {"detail": 'El campo "acudiente" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            acudiente_instancia = Acudiente.objects.get(id_acudiente=id_acudiente)
        except Acudiente.DoesNotExist:
            return Response(
                {"detail": "El acudiente especificado no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Verificar si el usuario ya existe
        username = data.get('numero_documento', '')
        if CustomUser.objects.filter(username=username).exists():
            return Response({'detail': 'El numero de identificacion ya esta registrado'}, status=status.HTTP_400_BAD_REQUEST)

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
                    acudiente=acudiente_instancia,
                    ciudad_residencia=data.get('ciudad_residencia'),
                    eps=data.get('eps'),
                    grado=data.get('grado'),
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
                    descripcion_discapacidad=data.get('descripcion_discapacidad'),
                    documento_identidad=request.FILES.get('documento_identidad'),
                    recibo_pago=request.FILES.get('recibo_pago'),
                    foto=request.FILES.get('foto'),
                    constancia_estudios=request.FILES.get('constancia_estudios'),
                )

            # Puedes retornar la información deseada
            return Response({'detail': 'Estudiante creado exitosamente'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Error al crear estudiante: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Actualizar un estudiante",
        operation_description="Actualiza todos los campos de un estudiante existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos del estudiante actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un estudiante",
        operation_description="Actualiza uno o más campos de un estudiante existente"
    )
    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy() 
        instance = self.get_object()
        user = instance.user
        
        # Manejar la contraseña si está presente
        if 'contrasena' in data and data['contrasena']:
            new_password = data.pop('contrasena') 
            user.set_password(new_password)
            user.save()
            hashed_password = make_password(new_password)
            instance.contrasena = hashed_password
            instance.save()
            
        #Manejar is_active
        if 'is_active' in data:
            is_active = data.pop('is_active')
            user.is_active = is_active
            user.save()
            instance.is_active = is_active
            instance.save()
        
        #Manejar el nombre de usuario
        if 'nombre' in data:
            nombre = data.pop('nombre')
            user.first_name = nombre
            user.save()
            instance.nombre = nombre
            instance.save()
            
        #Manejar el apellido
        if 'apellido' in data:
            apellido = data.pop('apellido')
            user.last_name = apellido
            user.save()
            instance.apellido = apellido
            instance.save()
        
        #Manejar el email
        if 'email' in data:
            email = data.pop('email')
            user.email = email
            user.save()
            instance.email = email
            instance.save()
        
        if data:
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            # Si solo se cambió la contraseña y no hay otros campos, devolvemos los datos actualizados
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
    
    def get_s3_client(self):
        """
        Retorna un cliente de boto3 para S3 usando las variables de entorno.
        """
        return boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', ''),
            region_name=os.getenv('AWS_S3_REGION_NAME', 'us-east-1'),
    )
    
    @swagger_auto_schema(
        operation_summary="Eliminar un estudiante",
        operation_description="Elimina permanentemente un estudiante del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = None
        s3 = self.get_s3_client()
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', 'archivos-estudiantes')

        archivos = [
            instance.documento_identidad,
            instance.recibo_pago,
            instance.foto,
            instance.constancia_estudios,
        ]
        for archivo in archivos:
            if archivo and hasattr(archivo, 'name') and archivo.name:
                key = f"media/{archivo.name.lstrip('/')}"  # Asegura el prefijo correcto
                try:
                    print(f"Eliminando archivo {key} de S3...")
                    s3.delete_object(Bucket=bucket_name, Key=key)
                except Exception as e:
                    print(f"Error eliminando archivo {key} de S3: {str(e)}")

        try:
            user = instance.user
        except Exception:
            pass

        self.perform_destroy(instance)
        if user:
            try:
                from rest_framework.authtoken.models import Token
                Token.objects.filter(user=user).delete()
                user.delete()
            except Exception as e:
                print(f"Error eliminando usuario: {str(e)}")
        # Retorna respuesta exitosa sin llamar a super().destroy()
        return Response({"detail": "Estudiante y archivos eliminados correctamente."}, status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary="Comprobar la conexión con Amazon S3",
        operation_description="Establece una conexión con Amazon S3 y retorna un mensaje de éxito o error"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrador])
    def conexion_s3(self, request):
        """
        Establece la conexión con Amazon S3.
        """
        try:
            s3 = self.get_s3_client()
            # Verificar si el bucket existe
            s3.head_bucket(Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME', 'archivos-estudiantes'))
            return Response({"detail": "Conexión exitosa a Amazon S3"}, status=status.HTTP_200_OK)
        except NoCredentialsError:
            return Response({"detail": "Credenciales de AWS no válidas"}, status=status.HTTP_400_BAD_REQUEST)
        except ClientError as e:
            return Response({"detail": f"Error al conectar con S3: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        operation_summary="Eliminar estudiantes por lote",
        operation_description="Elimina varios estudiantes y sus archivos de S3. Recibe una lista de IDs.",
        request_body=LoteEliminarSerializer,
        responses={200: 'Estudiantes eliminados correctamente', 400: 'Error en la solicitud'}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAdministrador])
    def eliminar_lote(self, request):
        serializer = LoteEliminarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ids = serializer.validated_data['ids']
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', ''),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', ''),
            region_name=os.getenv('AWS_S3_REGION_NAME', 'us-east-1'),
        )
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', 'archivos-estudiantes')

        eliminados = []
        errores = []
        for id_est in ids:
            try:
                estudiante = Estudiante.objects.get(pk=id_est)
                archivos = [
                    estudiante.documento_identidad,
                    estudiante.recibo_pago,
                    estudiante.foto,
                    estudiante.constancia_estudios,
                ]
                for archivo in archivos:
                    if archivo and hasattr(archivo, 'name') and archivo.name:
                        key = f"media/{archivo.name.lstrip('/')}"
                        try:
                            s3.delete_object(Bucket=bucket_name, Key=key)
                        except Exception as e:
                            print(f"Error eliminando archivo {key} de S3: {str(e)}")
                user = getattr(estudiante, 'user', None)
                estudiante.delete()
                if user:
                    try:
                        from rest_framework.authtoken.models import Token
                        Token.objects.filter(user=user).delete()
                        user.delete()
                    except Exception as e:
                        print(f"Error eliminando usuario: {str(e)}")
                eliminados.append(id_est)
            except Estudiante.DoesNotExist:
                errores.append(id_est)
        
        return Response({
            "eliminados": eliminados,
            "no_encontrados": errores,
            "detail": "Proceso de eliminación por lote finalizado."
        }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='export-excel',
            permission_classes=[IsAdministrador])
    def export_excel(self, request):
        estudiantes = Estudiante.objects.all().select_related('acudiente')
        data = []
        for estudiante in estudiantes:
            row = {
                'nombre': estudiante.nombre,
                'apellido': estudiante.apellido,
                'numero_documento': estudiante.numero_documento,
                'email': estudiante.email,
                'ciudad_residencia': estudiante.ciudad_residencia,
                'eps': estudiante.eps,
                'grado': estudiante.grado,
                'tipo_documento': estudiante.tipo_documento,
                'genero': estudiante.genero,
                'fecha_nacimiento': estudiante.fecha_nacimiento,
                'telefono_fijo': estudiante.telefono_fijo,
                'celular': estudiante.celular,
                'departamento_residencia': estudiante.departamento_residencia,
                'comuna_residencia': estudiante.comuna_residencia,
                'direccion_residencia': estudiante.direccion_residencia,
                'estamento': estudiante.estamento,
                'discapacidad': estudiante.discapacidad,
                'tipo_discapacidad': estudiante.tipo_discapacidad,
                'descripcion_discapacidad': estudiante.descripcion_discapacidad,
            }
            # Agrega los datos del acudiente al final
            acudiente = estudiante.acudiente
            if acudiente:
                row['acudiente_nombre'] = acudiente.nombre_acudiente
                row['acudiente_apellido'] = acudiente.apellido_acudiente
                row['acudiente_tipo_documento'] = acudiente.tipo_documento_acudiente
                row['acudiente_numero_documento'] = acudiente.numero_documento_acudiente
                row['acudiente_celular'] = acudiente.celular_acudiente
            else:
                row['acudiente_nombre'] = ''
                row['acudiente_apellido'] = ''
                row['acudiente_tipo_documento'] = ''
                row['acudiente_numero_documento'] = ''
                row['acudiente_celular'] = ''
            data.append(row)

        df = pd.DataFrame(data)
        filename = f'estudiantes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        df.to_excel(response, index=False)
        return response
    
    #Filtros
    @swagger_auto_schema(
        operation_summary="Filtrar estudiantes por género",
        operation_description="Filtra los estudiantes por género especificado en los parámetros de la solicitud"
    )
    @action(detail=False, methods=['get'], url_path='filtro-genero',
            permission_classes=[IsAdministrador])
    def filtro_genero(self, request, *args, **kwargs):
        
        genero = request.query_params.get('genero', None)
        queryset = self.get_queryset()
        if genero:
            queryset = queryset.filter(genero=genero)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Filtrar estudiantes por estamento",
        operation_description="Filtra los estudiantes por estamento especificado en los parámetros de la solicitud"
    )
    @action(detail=False, methods=['get'], url_path='filtro-estamento',
            permission_classes=[IsAdministrador])
    def filtro_estamento(self, request, *args, **kwargs):
        
        estamento = request.query_params.get('estamento', None)
        queryset = self.get_queryset()
        if estamento:
            queryset = queryset.filter(estamento=estamento)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)