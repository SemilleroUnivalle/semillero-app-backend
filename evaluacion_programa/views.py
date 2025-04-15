from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import EvaluacionPrograma
#Serializadores
from .serializers import EvaluacionProgramaSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class EvaluacionProgramaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar la evaluacion del programa.
    
    Permite listar, crear, actualizar y eliminar la evaluacion del programa.
    """
    queryset = EvaluacionPrograma.objects.all()
    serializer_class = EvaluacionProgramaSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los la evaluacion del programa",
        operation_description="Retorna una lista de todos los la evaluacion del programa registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando la evaluacion del programa")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear una evaluacion de programa",
        operation_description="Crea un nuevo registro dna evaluacion de programa",
        responses={
            status.HTTP_201_CREATED: EvaluacionProgramaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creandna evaluacion de programa con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Evaluacion del programa creada exitosamente")

        #Responder con los datos del nuevna evaluacion de programa
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una evaluacion de programa específico",
        operation_description="Retorna los detalles de una evaluacion de programa específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una evaluacion de programa",
        operation_description="Actualiza todos los campos de una evaluacion de programa existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna evaluacion de programa con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Evaluacion del programa actualizado exitosamente")

        #Responder con los datos dena evaluacion de programa actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una evaluacion de programa",
        operation_description="Actualiza uno o más campos de una evaluacion de programa existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una evaluacion de programa",
        operation_description="Elimina permanentemente una evaluacion de programa del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)