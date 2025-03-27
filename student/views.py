from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Student
from .serializers import StudentSerializer, StudentLoginSerializer

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

class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

