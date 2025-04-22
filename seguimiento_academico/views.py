from rest_framework import viewsets, status
from rest_framework.response import Response

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import SeguimientoAcademico
#Serializadores
from .serializers import SeguimientoAcademicoSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated
#Permisos
from cuenta.permissions import IsEstudiante, IsProfesor, IsAdministrador, IsProfesorOrAdministrador


class SeguimientoAcademicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los seguimiento academico.
    
    Permite listar, crear, actualizar y eliminar el SeguimientoAcademico.
    """
    queryset = SeguimientoAcademico.objects.all()
    serializer_class = SeguimientoAcademicoSerializer
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
        operation_summary="Listar todos los seguimiento academico",
        operation_description="Retorna una lista de todos los seguimiento academico registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando los seguimiento academico")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un SeguimientoAcademico",
        operation_description="Crea un nuevo registro de SeguimientoAcademico",
        responses={
            status.HTTP_201_CREATED: SeguimientoAcademicoSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando un SeguimientoAcademico, con datos: {data}")

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("SeguimientoAcademico creada exitosamente")

        #Responder con los datos del nuevna SeguimientoAcademico",
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener una SeguimientoAcademico específico",
        operation_description="Retorna los detalles de una SeguimientoAcademico, específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar una SeguimientoAcademico",        
        operation_description="Actualiza todos los campos de una SeguimientoAcademico, existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizandna SeguimientoAcademico, con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("SeguimientoAcademico actualizado exitosamente")

        #Responder con los datos dena SeguimientoAcademico", actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente una SeguimientoAcademico",
        operation_description="Actualiza uno o más campos de una SeguimientoAcademico, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una SeguimientoAcademico",
        operation_description="Elimina permanentemente una SeguimientoAcademico, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)