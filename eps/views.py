from rest_framework import viewsets,status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import EPS
#Serializador
from .serializers import EPSSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador

class EPSViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar EPS de estudiantes
    Permite listar, crear, actualizar y eliminar EPS.
    """
    queryset = EPS.objects.all()
    serializer_class = EPSSerializer
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
        operation_summary="Listar todas las EPS",
        responses={200: EPSSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No hay EPS registradas"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear una nueva EPS",
        operation_description="Crea una nueva EPS con los datos proporcionados",
        request_body=EPSSerializer,
        responses={201: EPSSerializer,},
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando EPS con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("EPS creada exitosamente")

        #Responder con los datos de la nueva asistencia
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="Obtener una EPS específica",
        operation_description="Retorna los detalles de una EPS específica por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una EPS existente",
        operation_description="Actualiza los datos de una EPS existente",
        responses={
            status.HTTP_200_OK: EPSSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos",
            status.HTTP_404_NOT_FOUND: "EPS no encontrada",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Eliminar una EPS existente",
        operation_description="Elimina una EPS existente por su ID",
        responses={
            status.HTTP_204_NO_CONTENT: "EPS eliminada exitosamente",
            status.HTTP_404_NOT_FOUND: "EPS no encontrada"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)