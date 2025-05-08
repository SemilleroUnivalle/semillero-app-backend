from rest_framework import viewsets,status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Discapacidad
#Serializador
from .serializers import DiscapacidadSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador

class DiscapacidadViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar discapacidades de estudiantes
    Permite listar, crear, actualizar y eliminar discapacidades.
    """
    queryset = Discapacidad.objects.all()
    serializer_class = DiscapacidadSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos según la acción solicitada:
        - create: Estudiantes y administradores pueden crear
        - list, retrieve, update, partial_update, destroy: Solo administradores
        """
        if self.action == 'create':
            # Estudiantes y administradores pueden crear acudientes
            permission_classes = [IsEstudiante | IsAdministrador]
        else:
            # Solo administradores pueden listar, ver detalles, actualizar y eliminar
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary="Listar todas las discapacidaddes",
        responses={200: DiscapacidadSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        Listar todas las discapacidaddes.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_summary="Crear una nueva discapacidad",
        request_body=DiscapacidadSerializer,
        responses={201: DiscapacidadSerializer},
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Responder con los datos de la nueva asistencia
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="Obtener una discacidad específica",
        operation_description="Retorna los detalles de una discapacidad específica por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Actualizar una discapacidad",
        operation_description="Actualiza los datos de una discapacidad existente",
        responses={
            status.HTTP_200_OK: DiscapacidadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos",
            status.HTTP_404_NOT_FOUND: "Asistencia no encontrada"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Eliminar una dsicapacidad",
        operation_description="Elimina una discapacidad existente por su ID",
        responses={
            status.HTTP_204_NO_CONTENT: "discapacidad eliminada exitosamente",
            status.HTTP_404_NOT_FOUND: "discapacidad no encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)