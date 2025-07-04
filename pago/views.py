from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Pago
#Serializadores
from .serializers import PagoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsAdministrador, IsEstudianteOrAdministrador


class PagoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los pagos.
    
    Permite listar, crear, actualizar y eliminar el Pago.
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos según la acción solicitada:
        - create: Estudiantes y administradores pueden crear
        - list, retrieve, update, partial_update, destroy: Solo administradores
        """
        if self.action == 'create':
            # Estudiantes y administradores pueden crear acudientes
            permission_classes = [IsEstudianteOrAdministrador]
        else:
            # Solo administradores pueden listar, ver detalles, actualizar y eliminar
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los pagos",
        operation_description="Retorna una lista de todos los pagos registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un Pago",
        operation_description="Crea un nuevo registro de Pago",
        responses={
            status.HTTP_201_CREATED: PagoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Responder con los datos del nuevna Pago",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una Pago específico",
        operation_description="Retorna los detalles de una Pago, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una Pago",        
        operation_description="Actualiza todos los campos de una Pago, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        #Responder con los datos dena Pago", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una Pago",
        operation_description="Actualiza uno o más campos de una Pago, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una Pago",
        operation_description="Elimina permanentemente una Pago, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)