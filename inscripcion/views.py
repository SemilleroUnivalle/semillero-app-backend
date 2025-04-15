from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Inscripcion
#Serializadores
from .serializers import InscripcionSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Inscripciones.
    
    Permite listar, crear, actualizar y eliminar el inscripcion.
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Inscripciones",
        operation_description="Retorna una lista de todos los Inscripciones registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los Inscripciones")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un inscripcion",
        operation_description="Crea un nuevo registro de inscripcion",
        responses={
            status.HTTP_201_CREATED: InscripcionSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un inscripcion, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("inscripcion creada exitosamente")

        #Responder con los datos del nuevna inscripcion",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una inscripcion específico",
        operation_description="Retorna los detalles de una inscripcion, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una inscripcion",        
        operation_description="Actualiza todos los campos de una inscripcion, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna inscripcion, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("inscripcion actualizado exitosamente")

        #Responder con los datos dena inscripcion", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una inscripcion",
        operation_description="Actualiza uno o más campos de una inscripcion, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una inscripcion",
        operation_description="Elimina permanentemente una inscripcion, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)