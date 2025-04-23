from rest_framework import viewsets, status
from rest_framework.response import Response

# Documentación
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Modelo
from .models import OfertaCategoria
# Serializadores
from .serializers import OfertaCategoriaReadSerializer, OfertaCategoriaWriteSerializer
# Autenticación
from rest_framework.permissions import IsAuthenticated
# Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class OfertaCategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Oferta categoria.
    
    Permite listar, crear, actualizar y eliminar el Oferta categoria.
    """
    queryset = OfertaCategoria.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según el método:
        - Para GET (list, retrieve): OfertaCategoriaReadSerializer con depth=1
        - Para POST, PUT, PATCH: OfertaCategoriaWriteSerializer sin depth
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return OfertaCategoriaWriteSerializer
        return OfertaCategoriaReadSerializer

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
        operation_description="Retorna una lista de todos los Oferta categoria registrados",
        responses={
            status.HTTP_200_OK: OfertaCategoriaReadSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        print("Listando los Oferta categoria")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un Oferta categoria",
        operation_description="Crea un nuevo registro de Oferta categoria",
        request_body=OfertaCategoriaWriteSerializer,
        responses={
            status.HTTP_201_CREATED: OfertaCategoriaReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Hacemos una copia para no modificar el original
        print(f"Creando un Oferta categoria, con datos: {data}")
        
        # Crear el objeto usando el serializador de escritura
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        
        print("Oferta categoria creada exitosamente")
        
        # Usar el serializador de lectura para devolver la respuesta con depth=1
        read_serializer = OfertaCategoriaReadSerializer(instance)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
    
    @swagger_auto_schema(
        operation_summary="Obtener una Oferta categoria específico",
        operation_description="Retorna los detalles de una Oferta categoria, específico por su ID",
        responses={
            status.HTTP_200_OK: OfertaCategoriaReadSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una Oferta categoria",        
        operation_description="Actualiza todos los campos de una Oferta categoria, existente",
        request_body=OfertaCategoriaWriteSerializer,
        responses={
            status.HTTP_200_OK: OfertaCategoriaReadSerializer
        }
    )
    def update(self, request, *args, **kwargs):
        data = request.data.copy()  # Hacemos una copia para no modificar el original
        print(f"Actualizando una Oferta categoria, con ID {kwargs['pk']} y datos: {data}")
        
        # Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        
        print("Oferta categoria actualizado exitosamente")
        
        # Usar el serializador de lectura para devolver la respuesta con depth=1
        read_serializer = OfertaCategoriaReadSerializer(instance)
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        return serializer.save()
    
    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una Oferta categoria",
        operation_description="Actualiza uno o más campos de una Oferta categoria, existente",
        request_body=OfertaCategoriaWriteSerializer,
        responses={
            status.HTTP_200_OK: OfertaCategoriaReadSerializer
        }
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