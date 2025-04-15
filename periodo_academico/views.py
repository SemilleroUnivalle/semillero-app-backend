from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import PeriodoAcademico
#Serializadores
from .serializers import PeriodoAcademicoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class PeriodoAcademicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los periodod academico.
    
    Permite listar, crear, actualizar y eliminar el PeriodoAcademico.
    """
    queryset = PeriodoAcademico.objects.all()
    serializer_class = PeriodoAcademicoSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los periodod academico",
        operation_description="Retorna una lista de todos los periodod academico registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los periodod academico")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un PeriodoAcademico",
        operation_description="Crea un nuevo registro de PeriodoAcademico",
        responses={
            status.HTTP_201_CREATED: PeriodoAcademicoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un PeriodoAcademico, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("PeriodoAcademico creada exitosamente")

        #Responder con los datos del nuevna PeriodoAcademico",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una PeriodoAcademico específico",
        operation_description="Retorna los detalles de una PeriodoAcademico, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una PeriodoAcademico",        
        operation_description="Actualiza todos los campos de una PeriodoAcademico, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna PeriodoAcademico, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("PeriodoAcademico actualizado exitosamente")

        #Responder con los datos dena PeriodoAcademico", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una PeriodoAcademico",
        operation_description="Actualiza uno o más campos de una PeriodoAcademico, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una PeriodoAcademico",
        operation_description="Elimina permanentemente una PeriodoAcademico, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)