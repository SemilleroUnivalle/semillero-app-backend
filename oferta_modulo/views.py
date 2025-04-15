from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import OfertaModulo
#Serializadores
from .serializers import OfertaModuloSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class OfertaModuloViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los oferta modulos.
    
    Permite listar, crear, actualizar y eliminar el OfertaModulo.
    """
    queryset = OfertaModulo.objects.all()
    serializer_class = OfertaModuloSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los oferta modulos",
        operation_description="Retorna una lista de todos los oferta modulos registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los oferta modulos")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un OfertaModulo",
        operation_description="Crea un nuevo registro de OfertaModulo",
        responses={
            status.HTTP_201_CREATED: OfertaModuloSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un OfertaModulo, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("OfertaModulo creada exitosamente")

        #Responder con los datos del nuevna OfertaModulo",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una OfertaModulo específico",
        operation_description="Retorna los detalles de una OfertaModulo, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una OfertaModulo",        
        operation_description="Actualiza todos los campos de una OfertaModulo, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna OfertaModulo, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("OfertaModulo actualizado exitosamente")

        #Responder con los datos dena OfertaModulo", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una OfertaModulo",
        operation_description="Actualiza uno o más campos de una OfertaModulo, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una OfertaModulo",
        operation_description="Elimina permanentemente una OfertaModulo, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)