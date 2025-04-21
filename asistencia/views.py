from rest_framework import viewsets,status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Asistencia
#Serializador
from .serializers import AsistenciaSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador

class AsistenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar asistencias de estudiantes.
    
    Permite listar, crear, actualizar y eliminar asistencias.
    """
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos según la acción solicitada:
        - create: Estudiantes y administradores pueden crear
        - list, retrieve, update, partial_update, destroy: Solo administradores
        """
        if self.action == 'create':
            # Estudiantes y administradores pueden crear acudientes
            permission_classes = [IsProfesor | IsAdministrador]
        else:
            # Solo administradores pueden listar, ver detalles, actualizar y eliminar
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todas las asistencias",
        operation_description="Retorna una lista de todas las asistencias registradas"
    )
    def list(self, request, *args, **kwargs):
        print("Listando asistencias")
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Crear una asistencia",
        operation_description="Crea un nuevo registro de asistencia",
        responses={
            status.HTTP_201_CREATED: AsistenciaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando asistencia con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Asistencia creada exitosamente")

        #Responder con los datos de la nueva asistencia
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="Obtener una asistencia específica",
        operation_description="Retorna los detalles de una asistencia específica por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Actualizar una asistencia",
        operation_description="Actualiza los datos de una asistencia existente",
        responses={
            status.HTTP_200_OK: AsistenciaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos",
            status.HTTP_404_NOT_FOUND: "Asistencia no encontrada"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Eliminar una asistencia",
        operation_description="Elimina una asistencia existente por su ID",
        responses={
            status.HTTP_204_NO_CONTENT: "Asistencia eliminada exitosamente",
            status.HTTP_404_NOT_FOUND: "Asistencia no encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
