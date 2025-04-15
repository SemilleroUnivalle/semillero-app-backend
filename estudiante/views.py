from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Estudiante
#Serializadores
from .serializers import EstudianteSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated

class EstudianteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar estudiantes.
    
    Permite listar, crear, actualizar y eliminar estudiantes.
    """
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todos los estudiantes",
        operation_description="Retorna una lista de todos los estudiantes registrados"
    )
    def list(self, request, *args, **kwargs):
        print("Listando estudiantes")
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Crear un estudiante",
        operation_description="Crea un nuevo registro de estudiante",
        responses={
            status.HTTP_201_CREATED: EstudianteSerializer,
            status.HTTP_400_BAD_REQUEST: "Datos de entrada inválidos"
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        print(f"Creando estudiante con datos: {data}")

        # Usar identificación como contrasena si no se proporciona uno
        if 'contrasena' not in data or not data['contrasena']:
            data['contrasena'] = data.get('identificacion', '')
            print(f"Usando identificación como contrasena: {data['contrasena']}")
        
        # Hashear la contraseña antes de guardarla
        data['contrasena'] = make_password(data['contrasena'])

        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        print("Estudiante creado exitosamente")

        #Responder con los datos del nuevo estudiante
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Obtener un estudiante específico",
        operation_description="Retorna los detalles de un estudiante específico por su ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Actualizar un estudiante",
        operation_description="Actualiza todos los campos de un estudiante existente"
    )
    def update(self, request, *args, **kwargs):
        data = request.data
        print(f"Actualizando estudiante con ID {kwargs['pk']} y datos: {data}")

        #Actualizar el objeto usando el serializador
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print("Estudiante actualizado exitosamente")

        #Responder con los datos del estudiante actualizado
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Actualizar parcialmente un estudiante",
        operation_description="Actualiza uno o más campos de un estudiante existente"
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Eliminar un estudiante",
        operation_description="Elimina permanentemente un estudiante del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
