from rest_framework import viewsets, status
from rest_framework.response import Response
from modulo.models import Modulo
from django.http import JsonResponse
from auditlog.models import LogEntry
from .serializers import LogEntrySerializer
from auditlog.context import set_actor

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#Modelo
from .models import Inscripcion
from estudiante.models import Estudiante
#Serializadores
from .serializers import InscripcionSerializer, InscripcionInfProfeSerializer
#Autenticacion
from rest_framework.permissions import IsAuthenticated, AllowAny
#Permisos
from cuenta.permissions import IsAdministrador, IsEstudianteOrAdministrador, IsEstudianteOrAdministradorOrMonitorAdministrativo
#Actions
from rest_framework.decorators import action
#Dashboard
from django.db.models import Count, Value
from django.db.models.functions import Coalesce
from collections import OrderedDict

def file_update(instance, data, field_name):
        """
        Elimina el archivo anterior y asigna el nuevo si se envía uno.
        """
        uploaded_file = data.get(field_name)
        if uploaded_file:
            # Elimina el archivo anterior de S3 si existe
            old_file = getattr(instance, field_name, None)
            if old_file:
                old_file.delete(save=False)
            setattr(instance, field_name, uploaded_file)
            instance.save()
            data.pop(field_name)

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar los Inscripciones.
    
    Permite listar, crear, actualizar y eliminar el inscripcion.
    """
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Define permisos para todas las acciones:
        - Los administradores pueden realizar cualquier operación
        - Estudiantes pueden crear inscripciones
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsEstudianteOrAdministradorOrMonitorAdministrativo]
        else:
            permission_classes = [IsAdministrador]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Listar todos los Inscripciones",
        operation_description="Retorna una lista de todos los Inscripciones registrados"
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
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
        data = request.data.copy()

        id_modulo = data.get("id_modulo")
        if not id_modulo:
            return Response(
                {"detail": "id_modulo es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            modulo = Modulo.objects.get(id_modulo=id_modulo)
        except Modulo.DoesNotExist:
            return Response(
                {"detail": "El módulo no existe."},
                status=status.HTTP_404_NOT_FOUND
            )

        import sys
        #Tener el estado de oferta categoria y oferta academica
        oferta_categoria = modulo.id_oferta_categoria.get()
        oferta_academica = oferta_categoria.id_oferta_academica

        if oferta_categoria.estado or oferta_academica.estado:
            data["id_oferta_categoria"] = oferta_categoria.id_oferta_categoria
            data["oferta_academica"] = oferta_academica.id_oferta_academica
        else:
            return (Response({"detail": "La oferta categoria o academica no esta activa"}, status=status.HTTP_400_BAD_REQUEST))
        
        #Crear el objeto usando el serializador
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        #Responder con los datos de la nueva inscripción
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
        try:
            data = request.data.copy()  # Esto puede fallar con archivos grandes
            instance = self.get_object()

            file_update(instance, data, 'recibos_pago')
            file_update(instance, data, 'constancia')
            file_update(instance, data, 'certificado')

            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)
        except TypeError as e:
            # Este error ocurre si intentas copiar archivos grandes
            return Response(
                {"detail": "Error procesando archivos grandes.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Cubre cualquier otro error inesperado
            return Response(
                {"detail": "Ocurrió un error inesperado.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
    operation_summary="Actualizar parcialmente una inscripcion",
    operation_description="Actualiza uno o más campos de una inscripcion, existente"
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            instance = self.get_object()

            # Procesa archivos, pero puedes guardar el estado antes/después si lo deseas
            file_update(instance, data, 'recibos_pago')
            file_update(instance, data, 'constancia')
            file_update(instance, data, 'certificado')

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Compara datos originales con los nuevos
            changed = False
            for field, value in serializer.validated_data.items():
                if getattr(instance, field, None) != value:
                    changed = True
                    break

            # Si no hubo cambios, responde 204 o un mensaje personalizado
            if not changed:
                return Response(
                    {"detail": "No hubo cambios en la actualización."},
                    status=status.HTTP_204_NO_CONTENT  # O puedes usar 200 con mensaje
                )

            with set_actor(request.user): 
                self.perform_update(serializer)

            return Response(serializer.data)

        except TypeError as e:
            return Response(
                {"detail": "Error procesando archivos grandes.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Ocurrió un error inesperado.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
    
    #Utilizo perform update para actualizar el estado de la inscripción (No revisado, Revisado, Pendiente)
    def perform_update(self, serializer):
        instance = serializer.instance  # aún no ha guardado los cambios

        # Guarda valores originales
        recibo_pago_original = instance.verificacion_recibo_pago
        certificado_original = instance.verificacion_certificado
        #certificado = instance.verificacion_certificado

        # Guarda cambios nuevos
        instance = serializer.save()
        recibo_pago_nuevo = instance.verificacion_recibo_pago
        certificado_nuevo = instance.verificacion_certificado
        #certificado_nuevo = instance.verificacion_certificado

        # Asigna el estado correcto
        if recibo_pago_nuevo and certificado_nuevo:
            instance.estado = "Revisado"
        elif recibo_pago_nuevo or certificado_nuevo:
            instance.estado = "Pendiente"
        else:
            instance.estado = "No revisado"

        instance.save(update_fields=['estado'])

        # Busca el último logentry después de guardar
        logentry = LogEntry.objects.filter(
            object_id=instance.pk,
            content_type__model='inscripcion'
        ).order_by('-timestamp').first()

        # Solo actualiza el campo de auditoría si el valor fue cambiado
        if recibo_pago_original != recibo_pago_nuevo and logentry:
            instance.audit_documento_recibo_pago = logentry
        if certificado_original != certificado_nuevo and logentry:
            instance.audit_certificado = logentry
        
        # Guarda solo los campos que hayan cambiado
        campos_actualizados = []
        if recibo_pago_original != recibo_pago_nuevo:
            campos_actualizados.append('audit_documento_recibo_pago')
        if certificado_original != certificado_nuevo:
            campos_actualizados.append('audit_certificado')
        

        if campos_actualizados:
            instance.save(update_fields=campos_actualizados)
    
    @swagger_auto_schema(
        operation_summary="Eliminar una inscripcion",
        operation_description="Elimina permanentemente una inscripcion, del sistema"
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Elimina los archivos de S3 si existen
        if instance.recibo_pago:
            instance.recibo_pago.delete(save=False)
        if instance.constancia:
            instance.constancia.delete(save=False)
        if instance.certificado:
            instance.certificado.delete(save=False)
        # Ahora elimina la instancia del modelo
        return super().destroy(request, *args, **kwargs)

    #Filtros
    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por tipo de tipo de vinculacion",
        operation_description="Filtra la inscripcion por tipo de vinculacion especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-vinculacion',
            permission_classes=[IsAdministrador])
    def filtro_tipo_vinculacion(self, request, *args, **kwargs):
        tipo_vinculacion = request.query_params.get('tipo_vinculacion', None)
        queryset = self.get_queryset()
        if tipo_vinculacion:
            queryset = queryset.filter(tipo_vinculacion=tipo_vinculacion)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por estado (Activo o Inactivo)",
        operation_description="Filtra la inscripcion por estado especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-estado',
            permission_classes=[IsAdministrador])
    def filtro_estado(self, request, *args, **kwargs):
        estado = request.query_params.get('estado', None)
        queryset = self.get_queryset()
        if estado:
            queryset = queryset.filter(estado=estado)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por grupo",
        operation_description="Filtra la inscripcion por el grupo especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-grupo',
            permission_classes=[IsAdministrador])
    def filtro_grupo(self, request, *args, **kwargs):
        grupo = request.query_params.get('grupo', None)
        
        # Obtener queryset base y optimizar la consulta para Grupo y Profesor
        queryset = self.get_queryset().select_related('grupo', 'grupo__profesor') 

        if grupo:
            # Caso 1: Filtrar por grupos nulos
            if grupo.lower() in ['null', 'none']:
                # Aplica el filtro para registros donde el campo 'grupo' es NULL
                queryset = queryset.filter(grupo__isnull=True)
            
            # Caso 2: Filtrar por un ID de grupo específico
            else:
                # Filtra por el ID/valor del grupo
                # Usamos 'grupo__pk' para asegurar que filtramos por la clave foránea
                queryset = queryset.filter(grupo__pk=grupo)
            
        # El serializador InscripcionInfProfeSerializer mostrará el profesor
        serializer = InscripcionInfProfeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Filtrar inscripcion por estudiante",
        operation_description="Filtra la inscripcion por el estudiante especificado en los parámetros de la solicitud"
    )
    @action (detail=False, methods=['get'], url_path='filtro-estudiante',
            permission_classes=[IsAdministrador])
    def filtro_estudiante(self, request, *args, **kwargs):
        estudiante = request.query_params.get('id_estudiante', None)
        queryset = self.get_queryset()

        if estudiante:
            queryset = queryset.filter(id_estudiante=estudiante)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path="filtro-modulo",
            permission_classes=[IsAdministrador])
    def filtro_modulo(self, request):
        modulo = request.query_params.get('id_modulo', None)
        queryset = self.get_queryset()

        if modulo:
            queryset = queryset.filter(id_modulo=modulo)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    @action(detail=False, methods=['get'], url_path="auditoria-matricula",
            permission_classes=[IsAdministrador])
    def auditoria_inscripcion(self, request):
        logs = LogEntry.objects.all().order_by('-timestamp')[:100]
        serializer = LogEntrySerializer(logs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path="matricula-grupo",
            permission_classes=[IsAdministrador])
    def matricula_grupo(self, request):
        qs = Inscripcion.objects.select_related(
            'grupo', 
            'grupo__profesor',
            'grupo__monitor_academico',
            'id_estudiante', 
            'id_modulo', 
            'id_oferta_categoria'
        ).all().order_by('grupo_id', 'id_inscripcion')

        groups = OrderedDict()
        for ins in qs:
            gid = ins.grupo_id  # puede ser None
            
            if gid not in groups:
                
                if ins.grupo:
                    nombre_grupo = str(ins.grupo.nombre)
            
                    if ins.grupo.profesor:
                        profesor_data = {
                            'id': ins.grupo.profesor.id,
                            'nombre': str(ins.grupo.profesor.nombre) + " " + str(ins.grupo.profesor.apellido),
                        }
                        if ins.grupo.monitor_academico:
                            monitor_academico_data = {
                            'id' : ins.grupo.monitor_academico.id,
                            'nombre' : str(ins.grupo.monitor_academico.nombre) + " " + str(ins.grupo.monitor_academico.apellido),
                            }
                        else:
                            monitor_academico = None
                    else:
                        profesor_data = None 
                else:
                    # El grupo no existe (gid es None)
                    nombre_grupo = "NO ASIGNADO"
                    profesor_data = None # El profesor es nulo si no hay grupo

                groups[gid] = {
                    'grupo_id': gid,
                    'nombre': nombre_grupo,
                    'profesor': profesor_data,
                    'monitor': monitor_academico_data,
                    'matriculas': []
                }
                
            # serializamos cada inscripcion individualmente para incluir los campos calculados por el serializer
            groups[gid]['matriculas'].append(InscripcionSerializer(ins).data)

        # convertir a lista y añadir conteo
        result = []
        for g in groups.values():
            g['cantidad'] = len(g['matriculas'])
            result.append(g)

        return Response(result, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'], url_path="dashboard",
        permission_classes=[IsAdministrador])
    def dashboard(self, request):
        # totales
        total_enrollments = Inscripcion.objects.count()
        total_register = Estudiante.objects.count()
        active_modules = Modulo.objects.filter(estado=True).count()

        # inscripciones por módulo
        enrollments_by_module_qs = (
            Inscripcion.objects
            .filter(id_modulo__isnull=False)
            .values('id_modulo__nombre_modulo', 'id_modulo__id_area__nombre_area')
            .annotate(enrollments=Count('pk'))
            .order_by('-enrollments')
        )
        enrollments_by_module = [
            {
                "name": item['id_modulo__nombre_modulo'],
                "enrollments": item['enrollments'],
                "area": item['id_modulo__id_area__nombre_area'],
            }
            for item in enrollments_by_module_qs
        ]

        # inscripciones por estamento con porcentaje
        estamento_qs = (
            Inscripcion.objects
            .values(estamento=Coalesce('id_estudiante__estamento', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        enrollments_by_estamento = []
        for item in estamento_qs:
            count = item['count']
            percentage = round((count / total_enrollments) * 100) if total_enrollments else 0
            estamento = item['estamento'] or 'Desconocido'
            enrollments_by_estamento.append({
                "estamento": estamento.capitalize(),
                "count": count,
                "percentage": int(percentage),
            })

        # inscripciones por grado
        grade_qs = (
            Inscripcion.objects
            .values(grade=Coalesce('id_estudiante__grado', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        enrollments_by_grade = [
            {"grade": item['grade'], "count": item['count']}
            for item in grade_qs
        ]

        # inscripciones recientes (últimas 10)
        recent_qs = (
            Inscripcion.objects
            .select_related('id_estudiante', 'id_modulo')
            .order_by('-fecha_inscripcion')[:10]
        )
        recent_enrollments = []
        for ins in recent_qs:
            estudiante = ins.id_estudiante
            modulo = ins.id_modulo
            student_name = " ".join(filter(None, [getattr(estudiante, 'nombre', ''), getattr(estudiante, 'apellido', '')])).strip() if estudiante else ""
            module_name = getattr(modulo, 'nombre_modulo', None) if modulo else None
            status = getattr(ins, 'estado', None) or (getattr(estudiante, 'estado', None) if estudiante else 'No revisado')
            recent_enrollments.append({
                "id": ins.id_inscripcion,
                "studentName": student_name,
                "module": module_name,
                "date": ins.fecha_inscripcion.isoformat() if ins.fecha_inscripcion else None,
                "status": status,
            })

        # distribución por género
        gender_qs = (
            Inscripcion.objects
            .values(gender=Coalesce('id_estudiante__genero', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        gender_distribution = [
            {"gender": item['gender'], "count": item['count']}
            for item in gender_qs
        ]

        inscritosMatriculados = (total_enrollments / total_register) * 100
        inscritosNoMatriculados = abs((total_enrollments / total_register) - 1) * 100

        payload = {
            "totalEnrollments": total_enrollments,
            "totalRegister": total_register,
            "activeModules": active_modules,
            "enrollmentsByModule": enrollments_by_module,
            "enrollmentsByEstamento": enrollments_by_estamento,
            "enrollmentsByGrade": enrollments_by_grade,
            "recentEnrollments": recent_enrollments,
            "genderDistribution": gender_distribution,
            "inscritosMatriculados": inscritosMatriculados,
            "inscritosNoMatriculados":inscritosNoMatriculados,
        }

        return Response(payload)

    def asignar_grupos():
        pass

