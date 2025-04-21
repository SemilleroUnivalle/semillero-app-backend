from rest_framework import viewsets,status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Area
#Serializador
from .serializers import AreaSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador

class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar áreas.
    
    Permite listar, crear, actualizar y eliminar áreas.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todas las áreas",
        operation_description="Retorna una lista de todas las áreas registradas"
    )
    def list(self, request, *args, **kwargs):
        print("Listando áreas")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un área",
        operation_description="Crea un nuevo registro de área",
        responses={
            status.HTTP_201_CREATED: AreaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando área con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Área creada exitosamente")

        #Responder con los datos del nuevo área
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="Obtener un área específica",
        operation_description="Retorna los detalles de un área específica por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Actualizar un área",
        operation_description="Actualiza los datos de un área existente",
        responses={
            status.HTTP_200_OK: AreaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Eliminar un área",
        operation_description="Elimina un área existente por su ID",
        responses={
            status.HTTP_204_NO_CONTENT: "Área eliminada exitosamente",
            status.HTTP_404_NOT_FOUND: "Área no encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
        
