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

class PagoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los pagos.
    
    Permite listar, crear, actualizar y eliminar el Pago.
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los pagos",
        operation_description="Retorna una lista de todos los pagos registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los pagos")
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
        print(f"Creando un Pago, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Pago creada exitosamente")

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
        print(f"Actualizandna Pago, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Pago actualizado exitosamente")

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