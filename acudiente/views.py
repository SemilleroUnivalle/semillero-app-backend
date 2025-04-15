from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Acudiente
#Serializadores
from .serializers import AcudienteSerializer

class AcudienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar acudientes.
    
    Permite listar, crear, actualizar y eliminar acudientes.
    """
    queryset = Acudiente.objects.all()
    serializer_class = AcudienteSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los acudientes",
        operation_description="Retorna una lista de todos los acudientes registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando acudientes")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un acudiente",
        operation_description="Crea un nuevo registro de acudiente",
        responses={
            status.HTTP_201_CREATED: AcudienteSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando acudiente con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Acudiente creado exitosamente")

        #Responder con los datos del nuevo acudiente
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        operation_summary="Obtener un acudiente específico",
        operation_description="Retorna los detalles de un acudiente específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary="Actualizar un acudiente",
        operation_description="Actualiza los datos de un acudiente existente",
        responses={
            status.HTTP_200_OK: AcudienteSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizando acudiente con datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Acudiente actualizado exitosamente")

        #Responder con los datos del acudiente actualizado
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Eliminar un estudiante",
        operation_description="Elimina permanentemente un estudiante del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


