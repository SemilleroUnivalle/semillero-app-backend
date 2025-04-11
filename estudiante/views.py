from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Estudiante
#Serializadores
from .serializers import EstudianteSerializer, EstudianteInicioSesionSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class EstudianteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar estudiantes.
    
    Permite listar, crear, actualizar y eliminar estudiantes.
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los estudiantes",
        operation_description="Retorna una lista de todos los estudiantes registrados"
    )
    def list(self, request, *args, **kwargs):
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
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        Crea un estudiante utilizando el método create_user del manager.
        """
        data = serializer.validated_data
        Estudiante.objects.create_user(
            nombre=data['nombre'],
            apellido=data['apellido'],
            numero_identificacion=data['numero_identificacion'],
            email=data['email']
        )

    def perform_update(self, serializer):
        instance = serializer.instance
        validated_data = serializer.validated_data
        
        print(f"Campos a actualizar: {validated_data.keys()}")
        print(f"Valores actuales: {instance.__dict__}")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        print(f"Valores después de actualizar: {instance.__dict__}")
        return instance

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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            # Si la instancia tiene un caché de objetos prefetcheados, limpiarlo
            instance._prefetched_objects_cache = {}
        
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

class EstadoInscripcionView(APIView):
    """Vista para verificar el estado del registro de un estudiante"""
    #permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Estado de registro",
        operation_description="Obtiene el estado actual del registro del estudiante por su ID",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Estado del registro",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fase_actual': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'registro_completo': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'documentos_faltantes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: "Estudiante no encontrado"
        }
    )
    def get(self, request, estudiante_id):
        try:
            # Buscar el estudiante por su ID
            estudiante = Estudiante.objects.get(id=estudiante_id)
            
            # Verificar documentos faltantes
            documentos_faltantes = []
            if not estudiante.Foto:
                documentos_faltantes.append("Foto")
            if not estudiante.documento_identidad:
                documentos_faltantes.append("Documento de identidad")
            if not estudiante.constancia_estudios:
                documentos_faltantes.append("Constancia de estudios")
            if not estudiante.comprobante_pago:
                documentos_faltantes.append("Comprobante de pago")
            
            # Verificar campos de información personal obligatorios
            campos_faltantes = []
            if not estudiante.genero:
                campos_faltantes.append("Género")
            if not estudiante.fecha_nacimiento:
                campos_faltantes.append("Fecha de nacimiento")
            if not estudiante.telefono and not estudiante.celular:
                campos_faltantes.append("Teléfono o celular")
            if not estudiante.departamento_residencia:
                campos_faltantes.append("Departamento de residencia")
            if not estudiante.direccion:
                campos_faltantes.append("Dirección")
            
            return Response({
                'fase_actual': estudiante.registration_phase,
                'registro_completo': estudiante.registration_phase == 2,
                'documentos_faltantes': documentos_faltantes,
                'campos_faltantes': campos_faltantes
            }, status=status.HTTP_200_OK)
        except Estudiante.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class EstudianteInicioSesionView(APIView):
    @swagger_auto_schema(
        operation_summary="Login de estudiante",
        operation_description="Autentica a un estudiante y devuelve tokens JWT"
    )
    def post(self, request):
        serializer = EstudianteInicioSesionSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener el estudiante del serializer
            estudiante = serializer.validated_data['estudiante']
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(estudiante)
            
            # Preparar los campos de archivos
            foto_url = estudiante.Foto.url if estudiante.Foto else None
            documento_identidad_url = estudiante.documento_identidad.url if estudiante.documento_identidad else None
            constancia_estudios_url = estudiante.constancia_estudios.url if estudiante.constancia_estudios else None
            comprobante_pago_url = estudiante.comprobante_pago.url if estudiante.comprobante_pago else None
            
            return Response({
                # Tokens JWT
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                
                # Información básica
                'id': estudiante.id,
                'nombre': estudiante.nombre,
                'apellido': estudiante.apellido,
                'numero_identificacion': estudiante.numero_identificacion,
                'email': estudiante.email,
                'registration_phase': estudiante.registration_phase,
                
                # Información adicional
                'tipo_identificacion': estudiante.tipo_identificacion,
                'genero': estudiante.genero,
                'fecha_nacimiento': estudiante.fecha_nacimiento,
                'telefono': estudiante.telefono,
                'celular': estudiante.celular,
                'departamento_residencia': estudiante.departamento_residencia,
                'comuna': estudiante.comuna,
                'direccion': estudiante.direccion,
                'estamento': estudiante.estamento,
                'discapacidad': estudiante.discapacidad,
                'tipo_discapacidad': estudiante.tipo_discapacidad,
                'descripcion_discapacidad': estudiante.descripcion_discapacidad,
                
                # URLs de archivos
                'foto_url': foto_url,
                'documento_identidad_url': documento_identidad_url,
                'constancia_estudios_url': constancia_estudios_url,
                'comprobante_pago_url': comprobante_pago_url
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Si el cliente manda el refresh token, podemos intentar invalidarlo
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Intentamos invalidar el token
                try:
                    token = RefreshToken(refresh_token)
                    # Ajustar la fecha de expiración para invalidarlo inmediatamente
                    token.set_exp(lifetime=0)
                except TokenError:
                    pass  # Ignoramos errores con tokens inválidos
                
            # Independiente de si recibimos o no el token de refresco,
            # indicamos al cliente que debe eliminar sus tokens almacenados
            return Response({
                "detail": "Sesión cerrada correctamente. Por favor elimina los tokens almacenados.",
                "success": True
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": str(e),
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)

