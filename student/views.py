from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Student
#Serializadores
from .serializers import StudentSerializer, StudentLoginSerializer, StudentRegistrationPhase2Serializer, StudentPhase2FilesSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar estudiantes.
    
    Permite listar, crear, actualizar y eliminar estudiantes.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
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
            status.HTTP_201_CREATED: StudentSerializer,
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
        Student.objects.create_user(
            nombre=data['nombre'],
            apellido=data['apellido'],
            numero_identificacion=data['numero_identificacion'],
            email=data['email']
        )

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
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un estudiante",
        operation_description="Elimina permanentemente un estudiante del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class StudentRegisterPhase2View(APIView):
    """Vista para la segunda fase de registro de estudiantes"""
    #permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Registrar estudiante - Fase 2",
        operation_description="Completa el registro de un estudiante con información adicional",
        
    )
    def put(self, request, student_id):  # Añadir el parámetro student_id aquí
        try:
            
            # Buscar el estudiante por su ID
            student = Student.objects.get(id=student_id)
            
            # Verificar que el estudiante está en fase 1
            if student.registration_phase != 1:
                return Response({'error': 'Este estudiante ya ha completado su registro'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            serializer = StudentRegistrationPhase2Serializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                student = serializer.save()
                student.registration_phase = 2  # Actualizar a fase completada
                student.save()
                
                return Response({
                    'mensaje': 'Registro completado exitosamente'
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Student.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class StudentUploadFilesView(APIView):
    """Vista para la carga de archivos durante el registro"""
    #permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    @swagger_auto_schema(
        operation_summary="Cargar documentos del estudiante",
        operation_description="Carga los documentos requeridos para completar el registro",
        responses={
            status.HTTP_200_OK: openapi.Response("Archivos cargados exitosamente"),
            status.HTTP_400_BAD_REQUEST: "Datos inválidos",
            status.HTTP_404_NOT_FOUND: "Estudiante no encontrado"
        }
    )
    def post(self, request, student_id):
        try:
            # Buscar el estudiante por su ID
            student = Student.objects.get(id=student_id)
            
            # Verificar que el estudiante está en la fase adecuada
            if student.registration_phase == 2:
                return Response({'error': 'Este estudiante ya ha completado su registro'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            serializer = StudentPhase2FilesSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Verificar si ha cargado todos los documentos necesarios
                documentos_completos = all([
                    student.Foto, 
                    student.documento_identidad, 
                    student.constancia_estudios, 
                    student.comprobante_pago
                ])
                
                # Si ha cargado todos los documentos, completar registro
                if documentos_completos:
                    student.registration_phase = 2
                    student.save()
                    mensaje = "Registro completado exitosamente. Todos los documentos han sido cargados."
                else:
                    mensaje = "Documentos cargados exitosamente. Algunos documentos aún son requeridos para completar el registro."
                
                return Response({
                    'mensaje': mensaje,
                    'documentos_cargados': {
                        'foto': student.Foto is not None,
                        'documento_identidad': student.documento_identidad is not None,
                        'constancia_estudios': student.constancia_estudios is not None,
                        'comprobante_pago': student.comprobante_pago is not None
                    }
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Student.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class StudentRegistrationStatusView(APIView):
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
    def get(self, request, student_id):
        try:
            # Buscar el estudiante por su ID
            student = Student.objects.get(id=student_id)
            
            # Verificar documentos faltantes
            documentos_faltantes = []
            if not student.Foto:
                documentos_faltantes.append("Foto")
            if not student.documento_identidad:
                documentos_faltantes.append("Documento de identidad")
            if not student.constancia_estudios:
                documentos_faltantes.append("Constancia de estudios")
            if not student.comprobante_pago:
                documentos_faltantes.append("Comprobante de pago")
            
            # Verificar campos de información personal obligatorios
            campos_faltantes = []
            if not student.genero:
                campos_faltantes.append("Género")
            if not student.fecha_nacimiento:
                campos_faltantes.append("Fecha de nacimiento")
            if not student.telefono and not student.celular:
                campos_faltantes.append("Teléfono o celular")
            if not student.departamento_residencia:
                campos_faltantes.append("Departamento de residencia")
            if not student.direccion:
                campos_faltantes.append("Dirección")
            
            return Response({
                'fase_actual': student.registration_phase,
                'registro_completo': student.registration_phase == 2,
                'documentos_faltantes': documentos_faltantes,
                'campos_faltantes': campos_faltantes
            }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class StudentLoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Login de estudiante",
        operation_description="Autentica a un estudiante y devuelve tokens JWT"
    )
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener el estudiante del serializer
            student = serializer.validated_data['student']
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(student)
            
            # Preparar los campos de archivos
            foto_url = student.Foto.url if student.Foto else None
            documento_identidad_url = student.documento_identidad.url if student.documento_identidad else None
            constancia_estudios_url = student.constancia_estudios.url if student.constancia_estudios else None
            comprobante_pago_url = student.comprobante_pago.url if student.comprobante_pago else None
            
            return Response({
                # Tokens JWT
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                
                # Información básica
                'id': student.id,
                'nombre': student.nombre,
                'apellido': student.apellido,
                'numero_identificacion': student.numero_identificacion,
                'email': student.email,
                'registration_phase': student.registration_phase,
                
                # Información adicional
                'tipo_identificacion': student.tipo_identificacion,
                'genero': student.genero,
                'fecha_nacimiento': student.fecha_nacimiento,
                'telefono': student.telefono,
                'celular': student.celular,
                'departamento_residencia': student.departamento_residencia,
                'comuna': student.comuna,
                'direccion': student.direccion,
                'estamento': student.estamento,
                'discapacidad': student.discapacidad,
                'tipo_discapacidad': student.tipo_discapacidad,
                'descripcion_discapacidad': student.descripcion_discapacidad,
                
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

