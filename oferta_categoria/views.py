from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from collections import defaultdict

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
    API endpoint para gestionar los oferta categoria.
    
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
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un Oferta categoria",
        operation_description="Crea un nuevo registro de Oferta categoria",
        request_body=OfertaCategoriaWriteSerializer,
        responses={
            status.HTTP_201_CREATED: OfertaCategoriaWriteSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Crear una nueva OfertaCategoria.
        """
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()  # Llama al método `create` del serializador

        # Usar el serializador de lectura para la respuesta
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
        """
        Actualizar una OfertaCategoria existente.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()  # Llama al método `update` del serializador

        # Usar el serializador de lectura para la respuesta
        read_serializer = OfertaCategoriaReadSerializer(instance)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

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
    
    @swagger_auto_schema(
        operation_summary="Obtener OfertaCategoria agrupadas por OfertaAcademica",
        operation_description="Retorna todas las OfertaCategoria agrupadas por OfertaAcademica",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Lista de OfertaCategoria agrupadas por OfertaAcademica",
                examples={
                    "application/json": {
                        "oferta_academica_1": [
                            {
                                "id": 1,
                                "nombre": "Oferta Categoria 1"
                            },
                            {
                                "id": 2,
                                "nombre": "Oferta Categoria 2"
                            }
                        ],
                        "oferta_academica_2": [
                            {
                                "id": 3,
                                "nombre": "Oferta Categoria 3"
                            }
                        ]
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='por-oferta-academica')
    def obtener_oferta_categoria_por_oferta_academica(self, request):
        """
        Obtener todas las OfertaCategoria agrupadas por OfertaAcademica
        **solo donde la OfertaAcademica tiene estado='activo'**.
        """
        # Filtrar por estado activo
        queryset = self.get_queryset().filter(id_oferta_academica__estado='activo')
        oferta_categoria_por_oferta_academica = defaultdict(list)

        for oferta_categoria in queryset:
            key = str(oferta_categoria.id_oferta_academica_id)  # Usar el ID como string para la clave
            oferta_categoria_por_oferta_academica[key].append(oferta_categoria)

        # Serializar cada grupo por separado
        resultado = {}
        for key, items in oferta_categoria_por_oferta_academica.items():
            serializer = OfertaCategoriaReadSerializer(items, many=True)
            resultado[key] = serializer.data

        return Response(resultado, status=status.HTTP_200_OK)
        