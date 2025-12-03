from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from collections import defaultdict

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Modulo
#Serializadores
from .serializers import ModuloReadSerializer, ModuloWriteSerializer, ModuloReadIdNombreSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class ModuloViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Modulos.
    
    Permite listar, crear, actualizar y eliminar Modulos.
    """
    queryset = Modulo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Usa el serializador correcto según el método:
        - Para GET (list, retrieve): ModuloReadSerializer con depth=1
        - Para POST, PUT, PATCH: ModuloWriteSerializer sin depth
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ModuloWriteSerializer
        return ModuloReadSerializer

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Solo los administradores pueden realizar cualquier operación
        - Estudiantes y profesores no tienen acceso
        """
        permission_classes = [IsAuthenticated, IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los modulos",
        operation_description="Retorna todos los modulos registrados por el administrador"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un modulo",
        operation_description="Crea un nuevo modulo en el sistema",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_201_CREATED: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            # Obtener el objeto creado y devolverlo con el serializador de lectura
            instance = serializer.instance
            read_serializer = ModuloReadSerializer(instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Obtener un modulo específico",
        operation_description="Retorna los detalles de un modulo específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un modulo",        
        operation_description="Actualiza todos los campos de un modulo existente",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_200_OK: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
            # Devolver respuesta con el serializador de lectura para mostrar relaciones
            read_serializer = ModuloReadSerializer(instance)
            return Response(read_serializer.data)
        except ValidationError as e:
            return Response({"detalle": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un modulo",
        operation_description="Actualiza uno o más campos de un modulo existente",
        request_body=ModuloWriteSerializer,
        responses={
            status.HTTP_200_OK: ModuloReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un Modulo",
        operation_description="Elimina permanentemente un Modulo del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Listar módulos por categoría",
        operation_description="Retorna los módulos agrupados por categoría",
        manual_parameters=[
            openapi.Parameter(
                'solo_activos', 
                openapi.IN_QUERY, 
                description="Filtrar solo módulos activos (true/false)", 
                type=openapi.TYPE_BOOLEAN,
                default=True
            )
        ],
        responses={
            status.HTTP_200_OK: "Módulos agrupados por categoría",
            status.HTTP_204_NO_CONTENT: "No hay módulos registrados"
        }
    )
    @action(detail=False, methods=['get'], url_path='por-categoria')
    def listar_por_categoria(self, request):
        """
        Endpoint para listar los módulos agrupados por categoría.
        """
        solo_activos = request.query_params.get('solo_activos', 'true').lower() == 'true'
        
        # Obtener todos los módulos con sus categorías en una sola consulta
        queryset = Modulo.objects.select_related('id_categoria')
        
        if solo_activos:
            queryset = queryset.filter(estado=True)
            
        if not queryset.exists():
            return Response({"mensaje": "No hay módulos registrados"}, status=status.HTTP_204_NO_CONTENT)
        
        # Agrupar módulos por categoría
        modulos_por_categoria = defaultdict(list)
        categorias_info = {}  # Para almacenar información de las categorías

        for modulo in queryset:
            if modulo.id_categoria:
                # Serializar cada módulo
                serialized_modulo = ModuloReadSerializer(modulo).data
                
                # Obtener información de la categoría - extractar valores primitivos
                categoria_obj = modulo.id_categoria
                # Usar el id numérico como clave (valor primitivo)
                categoria_id = categoria_obj.id_categoria  # Asegúrate que este es el nombre correcto del campo ID
                categoria_nombre = categoria_obj.nombre if hasattr(categoria_obj, 'nombre') else str(categoria_obj)
                
                # Guardar info de la categoría usando el ID numérico como clave
                categorias_info[categoria_id] = {"id": categoria_id, "nombre": categoria_nombre}
                
                # Agrupar por ID de categoría (valor numérico)
                modulos_por_categoria[categoria_id].append(serialized_modulo)

        # Construir el resultado final con el formato deseado
        resultado = []
        for cat_id, modulos in modulos_por_categoria.items():
            cat_info = categorias_info[cat_id]
            
            # Crear un diccionario para esta categoría con sus propiedades y módulos
            categoria_con_modulos = {
                "id": cat_id,  # Ya tenemos el ID numérico directamente
                "nombre": cat_info["nombre"],
                "modulos": modulos
            }
            resultado.append(categoria_con_modulos)
        
        # Si no hay módulos con categoría, devolver mensaje específico
        if not resultado:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(resultado, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(
        operation_summary="Listar módulo solo con id y nombre",
        operation_description="Retorna los módulos agrupados por categoría con solo el id y el nombre",
        responses={
            status.HTTP_200_OK: "Módulos agrupados por categoría con solo el id y el nombre",
            status.HTTP_404_NOT_FOUND: "No se encontraron módulos"
        })
    @action(detail=False, methods=['get'], url_path='por-categoria-id-nombre')
    def list_modulos(self, request):
        activos = request.query_params.get('activos', 'true').lower() == 'true'

        if not activos:
            queryset = Modulo.objects.all()
        else:
            queryset = Modulo.objects.filter(estado=True)

        serializer = ModuloReadIdNombreSerializer(queryset, many=True)
        return Response(serializer.data)

        
        