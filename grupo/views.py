from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Grupo
#Serializadores
from .serializers import GrupoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class GrupoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los grupos.
    
    Permite listar, crear, actualizar y eliminar el grupo.
    """
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los grupos",
        operation_description="Retorna una lista de todos los grupos registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los grupos")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un grupo",
        operation_description="Crea un nuevo registro de grupo",
        responses={
            status.HTTP_201_CREATED: GrupoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un grupo, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("grupo creada exitosamente")

        #Responder con los datos del nuevna grupo",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una grupo específico",
        operation_description="Retorna los detalles de una grupo, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una grupo",        
        operation_description="Actualiza todos los campos de una grupo, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna grupo, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("grupo actualizado exitosamente")

        #Responder con los datos dena grupo", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una grupo",
        operation_description="Actualiza uno o más campos de una grupo, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una grupo",
        operation_description="Elimina permanentemente una grupo, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)