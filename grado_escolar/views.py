from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import GradoEscolar
#Serializadores
from .serializers import GradoEscolarSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class GradoEscolarViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar la grado escolar.
    
    Permite listar, crear, actualizar y eliminar la grado escolar.
    """
    queryset = GradoEscolar.objects.all()
    serializer_class = GradoEscolarSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los grados escolares",
        operation_description="Retorna una lista de todos los grados escolares registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los grados escolares")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un grado escolar",
        operation_description="Crea un nuevo registro dna grado escolar",
        responses={
            status.HTTP_201_CREATED: GradoEscolarSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un grado escolar, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("grado escolar creada exitosamente")

        #Responder con los datos del nuevna grado escolar",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una grado escolar específico",
        operation_description="Retorna los detalles de una grado escolar, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una grado escolar",        
        operation_description="Actualiza todos los campos de una grado escolar, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna grado escolar, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("grado escolar actualizado exitosamente")

        #Responder con los datos dena grado escolar", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una grado escolar",
        operation_description="Actualiza uno o más campos de una grado escolar, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una grado escolar",
        operation_description="Elimina permanentemente una grado escolar, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
