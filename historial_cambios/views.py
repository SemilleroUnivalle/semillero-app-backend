from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import HistorialCambios
#Serializadores
from .serializers import HistorialCambiosSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class HistorialCambiosViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los historiales de cambios.
    
    Permite listar, crear, actualizar y eliminar el historiald e cambios.
    """
    queryset = HistorialCambios.objects.all()
    serializer_class = HistorialCambiosSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los historiales de cambios",
        operation_description="Retorna una lista de todos los historiales de cambios registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los historiales de cambios")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un historiald e cambios",
        operation_description="Crea un nuevo registro de historiald e cambios",
        responses={
            status.HTTP_201_CREATED: HistorialCambiosSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un historiald e cambios, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("historiald e cambios creada exitosamente")

        #Responder con los datos del nuevna historiald e cambios",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una historiald e cambios específico",
        operation_description="Retorna los detalles de una historiald e cambios, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una historiald e cambios",        
        operation_description="Actualiza todos los campos de una historiald e cambios, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna historiald e cambios, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("historiald e cambios actualizado exitosamente")

        #Responder con los datos dena historiald e cambios", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una historiald e cambios",
        operation_description="Actualiza uno o más campos de una historiald e cambios, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una historiald e cambios",
        operation_description="Elimina permanentemente una historiald e cambios, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)