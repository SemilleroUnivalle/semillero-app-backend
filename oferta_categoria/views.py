from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import OfertaCategoria
#Serializadores
from .serializers import OfertaCategoriaSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class OfertaCategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Oferta categoria.
    
    Permite listar, crear, actualizar y eliminar el Oferta categoria.
    """
    queryset = OfertaCategoria.objects.all()
    serializer_class = OfertaCategoriaSerializer
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
        operation_summary="Listar todos los Oferta categoria",
        operation_description="Retorna una lista de todos los Oferta categoria registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los Oferta categoria")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un Oferta categoria",
        operation_description="Crea un nuevo registro de Oferta categoria",
        responses={
            status.HTTP_201_CREATED: OfertaCategoriaSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un Oferta categoria, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Oferta categoria creada exitosamente")

        #Responder con los datos del nuevna Oferta categoria",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una Oferta categoria específico",
        operation_description="Retorna los detalles de una Oferta categoria, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una Oferta categoria",        
        operation_description="Actualiza todos los campos de una Oferta categoria, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna Oferta categoria, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Oferta categoria actualizado exitosamente")

        #Responder con los datos dena Oferta categoria", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una Oferta categoria",
        operation_description="Actualiza uno o más campos de una Oferta categoria, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una Oferta categoria",
        operation_description="Elimina permanentemente una Oferta categoria, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)