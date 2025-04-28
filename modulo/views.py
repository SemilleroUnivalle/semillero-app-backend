from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Modulo
#Serializadores
from .serializers import ModuloSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class ModuloViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Modulos.
    
    Permite listar, crear, actualizar y eliminar el Modulo.
    """
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Modulos",
        operation_description="Retorna una lista de todos los Modulos registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los Modulos")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un Modulo",
        operation_description="Crea un nuevo registro de Modulo",
        responses={
            status.HTTP_201_CREATED: ModuloSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un Modulo, con datos: {data}")

        # Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            print("Modulo creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Capturar la excepción y devolver un error 400 con el mensaje
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Obtener una Modulo específico",
        operation_description="Retorna los detalles de una Modulo, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una Modulo",        
        operation_description="Actualiza todos los campos de una Modulo, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna Modulo, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Modulo actualizado exitosamente")

        #Responder con los datos dena Modulo", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una Modulo",
        operation_description="Actualiza uno o más campos de una Modulo, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una Modulo",
        operation_description="Elimina permanentemente una Modulo, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)