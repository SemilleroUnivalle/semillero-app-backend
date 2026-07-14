from rest_framework import viewsets, status
from rest_framework.response import Response
from modulo.models import Modulo
from profesor.models import Profesor
from monitor_academico.models import MonitorAcademico
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
from cuenta.permissions import IsAdministrador, IsEstudianteOrAdministrador, IsEstudianteOrAdministradorOrMonitorAdministrativo, IsProfesorOrAdministrador
#Actions
from rest_framework.decorators import action
#Dashboard
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, Lower
from collections import OrderedDict
#Geocodificacion
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

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
        elif self.action == 'filtro_estudiante':
            permission_classes = [IsEstudianteOrAdministrador]
        elif self.action == 'buscar_por_documento':
            permission_classes = [IsProfesorOrAdministrador]
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

        # # Resolver la oferta_categoria sin que lance MultipleObjectsReturned si pertenece a varias ofertas
        # oferta_academica_id = data.get("oferta_academica")
        # oferta_categoria_qs = modulo.id_oferta_categoria.all()
        
        # if oferta_academica_id:
        #     oferta_categoria_qs = oferta_categoria_qs.filter(id_oferta_academica=oferta_academica_id)
            
        # if not oferta_categoria_qs.exists():
        #     oferta_categoria_qs = modulo.id_oferta_categoria.filter(estado=True, id_oferta_academica__estado='inscripcion')
        # if not oferta_categoria_qs.exists():
        #     oferta_categoria_qs = modulo.id_oferta_categoria.filter(estado=True)
        # if not oferta_categoria_qs.exists():
        #     oferta_categoria_qs = modulo.id_oferta_categoria.all()
            
        # oferta_categoria = oferta_categoria_qs.first()
        # if not oferta_categoria:
        #     return Response({"detail": "El módulo no tiene una oferta de categoría asociada."}, status=status.HTTP_400_BAD_REQUEST)
            
        # oferta_academica = oferta_categoria.id_oferta_academica

        # if oferta_categoria.estado or oferta_academica.estado == 'inscripcion' or oferta_academica.estado == 'desarrollo':
        #     data["id_oferta_categoria"] = oferta_categoria.id_oferta_categoria
        #     data["oferta_academica"] = oferta_academica.id_oferta_academica
        # else:
        #     return Response({"detail": "La oferta categoria o academica no esta activa"}, status=status.HTTP_400_BAD_REQUEST)
        
        # nuevo

        # Resolver la oferta_categoria respetando la selección explícita del frontend
        oferta_categoria_id = data.get("id_oferta_categoria")
        oferta_academica_id = data.get("oferta_academica")

        if oferta_categoria_id:
            try:
                oferta_categoria_id = int(oferta_categoria_id)
            except (TypeError, ValueError):
                return Response(
                    {"detail": "id_oferta_categoria debe ser un número válido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            oferta_categoria = modulo.id_oferta_categoria.filter(
                pk=oferta_categoria_id
            ).first()

            if not oferta_categoria:
                return Response(
                    {"detail": "La oferta categoría enviada no existe o no está asociada al módulo."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif oferta_academica_id:
            try:
                oferta_academica_id = int(oferta_academica_id)
            except (TypeError, ValueError):
                return Response(
                    {"detail": "oferta_academica debe ser un número válido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            oferta_categoria_qs = modulo.id_oferta_categoria.filter(
                id_oferta_academica=oferta_academica_id
            )

            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.filter(
                    estado=True, id_oferta_academica__estado='inscripcion'
                )
            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.filter(estado=True)
            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.all()

            oferta_categoria = oferta_categoria_qs.first()

        else:
            oferta_categoria_qs = modulo.id_oferta_categoria.all()

            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.filter(estado=True, id_oferta_academica__estado='inscripcion')
            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.filter(estado=True)
            if not oferta_categoria_qs.exists():
                oferta_categoria_qs = modulo.id_oferta_categoria.all()

            oferta_categoria = oferta_categoria_qs.first()

        if not oferta_categoria:
            return Response(
                {"detail": "El módulo no tiene una oferta de categoría asociada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        oferta_academica = oferta_categoria.id_oferta_academica

        if oferta_categoria.estado or oferta_academica.estado == 'inscripcion' or oferta_academica.estado == 'desarrollo':
            data["id_oferta_categoria"] = oferta_categoria.id_oferta_categoria
            data["oferta_academica"] = oferta_academica.id_oferta_academica
        else:
            return Response(
                {"detail": "La oferta categoria o academica no esta activa"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        # Forzar que la constancia siempre sea True por requerimiento temporal
        data["verificacion_constancia"] = True

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

            file_update(instance, data, 'recibo_pago')
            file_update(instance, data, 'constancia')
            file_update(instance, data, 'certificado')
            file_update(instance, data, 'certificado_academico')
            file_update(instance, data, 'recibo_servicio')

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
            file_update(instance, data, 'recibo_pago')
            file_update(instance, data, 'constancia')
            file_update(instance, data, 'certificado')
            file_update(instance, data, 'certificado_academico')
            file_update(instance, data, 'recibo_servicio')

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
    
    # Utilizo perform update para actualizar el estado de la inscripción (No revisado, Revisado, Pendiente)
    def perform_update(self, serializer):
        instance = serializer.instance  # aún no ha guardado los cambios

        # Guarda valores originales de verificación para auditoría
        recibo_pago_original = instance.verificacion_recibo_pago
        constancia_original = instance.verificacion_constancia
        certificado_original = instance.verificacion_certificado
        recibo_servicio_original = instance.verificacion_recibo_servicio

        # Forzar que la constancia siempre sea True por requerimiento temporal
        serializer.validated_data['verificacion_constancia'] = True

        # Guarda cambios nuevos
        instance = serializer.save()
        
        # Obtenemos los valores actuales
        recibo_pago_nuevo = instance.verificacion_recibo_pago
        constancia_nuevo = instance.verificacion_constancia
        certificado_nuevo = instance.verificacion_certificado
        recibo_servicio_nuevo = instance.verificacion_recibo_servicio

        # Check if there are any uploaded files
        has_uploaded_files = bool(
            instance.recibo_pago or
            instance.constancia or
            instance.certificado or
            instance.recibo_servicio
        )

        estudiante_verificado = instance.id_estudiante.verificacion_informacion if instance.id_estudiante else False

        if has_uploaded_files:
            # Evaluamos el estado basándonos en documentos que existen
            documentos_verificados = []
            if instance.recibo_pago:
                documentos_verificados.append(recibo_pago_nuevo)
            if instance.constancia:
                documentos_verificados.append(constancia_nuevo)
            if instance.certificado:
                documentos_verificados.append(certificado_nuevo)
            if instance.recibo_servicio:
                documentos_verificados.append(recibo_servicio_nuevo)

            # Asigna el estado correcto
            if all(documentos_verificados) and estudiante_verificado:
                instance.estado = "Revisado"
            elif any(documentos_verificados) or estudiante_verificado:
                instance.estado = "Pendiente"
            else:
                instance.estado = "No revisado"
        else:
            # Si no hay archivos subidos, el estado depende de si el administrador
            # ha verificado explícitamente algún campo (excluyendo constancia que es forzada a True)
            verificaciones_manuales = [recibo_pago_nuevo, certificado_nuevo, recibo_servicio_nuevo]
            
            if any(verificaciones_manuales):
                if estudiante_verificado:
                    instance.estado = "Revisado"
                else:
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
        campos_actualizados = []
        if recibo_pago_original != recibo_pago_nuevo and logentry:
            instance.audit_documento_recibo_pago = logentry
            campos_actualizados.append('audit_documento_recibo_pago')
        if constancia_original != constancia_nuevo and logentry:
            instance.audit_constancia = logentry
            campos_actualizados.append('audit_constancia')
        if certificado_original != certificado_nuevo and logentry:
            instance.audit_certificado = logentry
            campos_actualizados.append('audit_certificado')
        if recibo_servicio_original != recibo_servicio_nuevo and logentry:
            instance.audit_recibo_servicio = logentry
            campos_actualizados.append('audit_recibo_servicio')

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
        if instance.certificado_academico:
            instance.certificado_academico.delete(save=False)
        if instance.recibo_servicio:
            instance.recibo_servicio.delete(save=False)
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
            permission_classes=[IsEstudianteOrAdministrador])
    def filtro_estudiante(self, request, *args, **kwargs):
        estudiante = request.query_params.get('id_estudiante', None)
        queryset = self.get_queryset()

        if estudiante:
            queryset = queryset.filter(id_estudiante=estudiante)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Buscar inscripciones por número de documento del estudiante",
        operation_description="Retorna las inscripciones del estudiante cuyo número de documento coincide con el parámetro enviado",
        manual_parameters=[
            openapi.Parameter(
                'numero_documento',
                openapi.IN_QUERY,
                description="Número de documento del estudiante",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'oferta_academica_id',
                openapi.IN_QUERY,
                description="ID de la oferta académica (opcional)",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='buscar-por-documento',
            permission_classes=[IsProfesorOrAdministrador])
    def buscar_por_documento(self, request, *args, **kwargs):
        numero_documento = request.query_params.get('numero_documento', None)

        if not numero_documento:
            return Response(
                {"detail": "El parámetro 'numero_documento' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Normalizar: quitar espacios al inicio/fin
        numero_documento = numero_documento.strip()

        # Verificar si el estudiante existe primero
        from estudiante.models import Estudiante
        estudiante_qs = Estudiante.objects.filter(numero_documento=numero_documento)
        if not estudiante_qs.exists():
            return Response(
                {"detail": f"No existe ningún estudiante con el número de documento '{numero_documento}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Buscar inscripciones del estudiante
        queryset = self.get_queryset().filter(
            id_estudiante__numero_documento=numero_documento
        ).select_related('id_estudiante', 'id_modulo', 'grupo', 'oferta_academica')

        # Filtro opcional por período académico
        oferta_academica_id = request.query_params.get('oferta_academica_id', None)
        if oferta_academica_id:
            queryset = queryset.filter(oferta_academica__id_oferta_academica=oferta_academica_id)

        if not queryset.exists():
            estudiante = estudiante_qs.first()
            return Response(
                {
                    "detail": f"El estudiante '{estudiante.nombre} {estudiante.apellido}' existe pero no tiene inscripciones registradas.",
                    "codigo": "SIN_INSCRIPCION",
                    "nombre": estudiante.nombre,
                    "apellido": estudiante.apellido,
                    "numero_documento": estudiante.numero_documento,
                },
                status=status.HTTP_404_NOT_FOUND
            )

        result = []
        for inscripcion in queryset:
            estudiante = inscripcion.id_estudiante
            result.append({
                "id_inscripcion": inscripcion.id_inscripcion,
                "nombre": estudiante.nombre,
                "apellido": estudiante.apellido,
                "numero_documento": estudiante.numero_documento,
                "modulo": inscripcion.id_modulo.nombre_modulo if inscripcion.id_modulo else None,
                "grupo": str(inscripcion.grupo) if inscripcion.grupo else None,
            })

        return Response(result, status=status.HTTP_200_OK)

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
        from grupo.models import Grupo
        all_groups = Grupo.objects.select_related('profesor', 'monitor_academico').all()
        
        groups = OrderedDict()
        for grupo in all_groups:
            gid = grupo.id
            nombre_grupo = str(grupo.nombre)
            periodo_nombre = grupo.oferta_academica.nombre if grupo.oferta_academica else "NO ASIGNADO"
            
            if grupo.profesor:
                profesor_data = {
                    'id': grupo.profesor.id,
                    'nombre': str(grupo.profesor.nombre) + " " + str(grupo.profesor.apellido),
                }
            else:
                profesor_data = None 

            if grupo.monitor_academico:
                monitor_academico_data = {
                    'id' : grupo.monitor_academico.id,
                    'nombre' : str(grupo.monitor_academico.nombre) + " " + str(grupo.monitor_academico.apellido),
                }
            else:
                monitor_academico_data = None

            groups[gid] = {
                'grupo_id': gid,
                'nombre': nombre_grupo,
                'periodo': periodo_nombre,
                'profesor': profesor_data,
                'monitor': monitor_academico_data,
                'matriculas': []
            }
        
        # Estudiantes sin grupo (gid = None)
        groups[None] = {
            'grupo_id': None,
            'nombre': "NO ASIGNADO",
            'periodo': "NO ASIGNADO",
            'profesor': None,
            'monitor': None,
            'matriculas': []
        }

        qs = Inscripcion.objects.select_related(
            'grupo', 
            'id_estudiante', 
            'id_modulo', 
            'id_oferta_categoria',
            'id_oferta_categoria__id_oferta_academica'
        ).all().order_by('grupo_id', 'id_inscripcion')

        for ins in qs:
            gid = ins.grupo_id  # puede ser None
            
            if gid not in groups:
                 # Backup para casos donde el grupo fue eliminado de la BD pero sigue en la inscripción (aunque no debería pasar por constraints)
                 pass
            
            # serializamos cada inscripcion individualmente
            if gid in groups or gid is None:
                groups[gid]['matriculas'].append(InscripcionSerializer(ins).data)
        
        # Para estudiantes sin grupo, tratar de ponerle un periodo basado en su oferta categoría
        for m in groups[None]['matriculas']:
            if 'oferta_categoria' in m and m['oferta_categoria'] and 'id_oferta_academica' in m['oferta_categoria']:
                groups[None]['periodo'] = m['oferta_categoria']['id_oferta_academica'].get('nombre', 'NO ASIGNADO')
                break

        # convertir a lista y añadir conteo
        result = []
        for g in groups.values():
            g['cantidad'] = len(g['matriculas'])
            result.append(g)

        return Response(result, status=status.HTTP_200_OK)



    @action(detail=False, methods=['get'], url_path="dashboard",
        permission_classes=[IsAdministrador])
    def dashboard(self, request):
        # Obtener parámetros de filtro
        periodo_id = request.query_params.get('periodo', None)
        modulo_id = request.query_params.get('modulo', None)
        area_id = request.query_params.get('area', None)
        tipo_vinculacion = request.query_params.get('tipo_vinculacion', None)
        estamento = request.query_params.get('estamento', None)

        # Base queryset para inscripciones con filtro opcional
        inscripciones_qs = Inscripcion.objects.all()
        estudiantes_qs = Estudiante.objects.all()

        # Filtrar inscripciones
        if periodo_id and periodo_id != 'all':
            inscripciones_qs = inscripciones_qs.filter(oferta_academica_id=periodo_id)
        if modulo_id and modulo_id != 'all' and modulo_id != '':
            inscripciones_qs = inscripciones_qs.filter(id_modulo_id=modulo_id)
        if area_id and area_id != 'all' and area_id != '':
            inscripciones_qs = inscripciones_qs.filter(id_modulo__id_area_id=area_id)
        if tipo_vinculacion and tipo_vinculacion != 'all' and tipo_vinculacion != '':
            inscripciones_qs = inscripciones_qs.filter(tipo_vinculacion__iexact=tipo_vinculacion)
        if estamento and estamento != 'all' and estamento != '':
            inscripciones_qs = inscripciones_qs.filter(id_estudiante__estamento__iexact=estamento)

        # Filtrar estudiantes registrados por periodo
        if periodo_id and periodo_id != 'all':
            try:
                from oferta_academica.models import OfertaAcademica
                periodo_actual = OfertaAcademica.objects.get(pk=periodo_id)
                siguiente_periodo = OfertaAcademica.objects.filter(
                    fecha_inicio__gt=periodo_actual.fecha_inicio
                ).order_by('fecha_inicio').first()

                if siguiente_periodo:
                    estudiantes_qs = estudiantes_qs.filter(
                        user__date_joined__gte=periodo_actual.fecha_inicio,
                        user__date_joined__lt=siguiente_periodo.fecha_inicio
                    )
                else:
                    estudiantes_qs = estudiantes_qs.filter(
                        user__date_joined__gte=periodo_actual.fecha_inicio
                    )
            except Exception as e:
                print(f"Error al filtrar por periodo: {e}")

        # Filtrar estudiantes registrados por estamento si aplica
        if estamento and estamento != 'all' and estamento != '':
            estudiantes_qs = estudiantes_qs.filter(estamento__iexact=estamento)

        # totales
        total_enrollments = inscripciones_qs.count()
        total_register = estudiantes_qs.count()
        active_modules = Modulo.objects.filter(estado=True).count()
        total_profesores = Profesor.objects.count()
        total_monitores = MonitorAcademico.objects.count()

        # inscripciones por módulo (usando el queryset filtrado)
        enrollments_by_module_qs = (
            inscripciones_qs
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

        # inscripciones por módulo y género (usando el queryset filtrado)
        enrollments_gender_qs = (
            inscripciones_qs
            .filter(id_modulo__isnull=False)
            .values(
                'id_modulo__nombre_modulo',
                gender=Coalesce(Lower('id_estudiante__genero'), Value('desconocido'))
            )
            .annotate(count=Count('pk'))
            .order_by('id_modulo__nombre_modulo', 'gender')
        )

        enrollments_by_module_and_gender = []
        current_module = None
        gender_breakdown = {}

        for item in enrollments_gender_qs:
            module_name = item['id_modulo__nombre_modulo']
            gender = item['gender'].capitalize() 
            count = item['count']

            if module_name != current_module:
                if current_module is not None:
                    enrollments_by_module_and_gender.append({
                        "moduleName": current_module,
                        "genderBreakdown": gender_breakdown
                    })
                
                current_module = module_name
                gender_breakdown = {}

            gender_breakdown[gender] = count

        if current_module is not None:
            enrollments_by_module_and_gender.append({
                "moduleName": current_module,
                "genderBreakdown": gender_breakdown
            })

        # inscripciones por estamento (usando el queryset filtrado)
        estamento_qs = (
            inscripciones_qs
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

        # inscripciones por grado (usando el queryset filtrado)
        grade_qs = (
            inscripciones_qs
            .values(grade=Coalesce('id_estudiante__grado', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        enrollments_by_grade = [
            {"grade": item['grade'], "count": item['count']}
            for item in grade_qs
        ]

        # inscripciones recientes (usando el queryset filtrado)
        recent_qs = (
            inscripciones_qs
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

        # distribución por género (usando el queryset filtrado)
        gender_qs = (
            inscripciones_qs
            .values(gender=Coalesce('id_estudiante__genero', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        gender_distribution = [
            {"gender": item['gender'], "count": item['count']}
            for item in gender_qs
        ]

        # distribución por estrato (usando el queryset filtrado)
        estrato_qs = (
            inscripciones_qs
            .values(estrato=Coalesce('id_estudiante__estrato', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        estrato_distribution = [
            {"estrato": item['estrato'] or 'Desconocido', "count": item['count']}
            for item in estrato_qs
        ]

        # distribución por vinculación (usando el queryset filtrado)
        vinculacion_qs = (
            inscripciones_qs
            .values(vinculacion=Coalesce('tipo_vinculacion', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        vinculacion_distribution = [
            {"type": item['vinculacion'], "count": item['count']}
            for item in vinculacion_qs
        ]

        # distribución por municipio (usando el queryset filtrado)
        municipio_qs = (
            inscripciones_qs
            .values(municipio=Coalesce('id_estudiante__ciudad_residencia', Value('Desconocido')))
            .annotate(count=Count('pk'))
            .order_by('-count')
        )
        municipio_distribution = [
            {"municipality": item['municipio'] or 'Desconocido', "count": item['count']}
            for item in municipio_qs
        ]

        # indicadores
        inscritosMatriculados = (total_enrollments / total_register * 100) if total_register > 0 else 0
        inscritosNoMatriculados = 100 - inscritosMatriculados if total_register > 0 else 0

        # Obtener detalle del periodo para el frontend
        periodo_detalle = None
        if periodo_id:
            try:
                from oferta_academica.models import OfertaAcademica
                from oferta_academica.serializers import OfertaAcademicaSerializer
                periodo_obj = OfertaAcademica.objects.get(pk=periodo_id)
                periodo_detalle = OfertaAcademicaSerializer(periodo_obj).data
            except:
                pass

        # Obtener opciones para los filtros de forma dinámica
        from area.models import Area
        modulos_options = list(Modulo.objects.filter(estado=True).values('id_modulo', 'nombre_modulo', 'id_area_id'))
        areas_options = list(Area.objects.filter(estado_area=True).values('id_area', 'nombre_area'))
        
        vinculaciones_unicas = list(Inscripcion.objects.values_list('tipo_vinculacion', flat=True).distinct())
        vinculaciones_options = sorted(list(set([v for v in vinculaciones_unicas if v])))
        
        estamentos_unicos = list(Estudiante.objects.values_list('estamento', flat=True).distinct())
        estamentos_options = sorted(list(set([e for e in estamentos_unicos if e])))

        payload = {
            "totalEnrollments": total_enrollments,
            "totalRegister": total_register,
            "activeModules": active_modules,
            "totalProfessors": total_profesores,
            "totalMonitors": total_monitores,
            "enrollmentsByModuleAndGender": enrollments_by_module_and_gender, 
            "enrollmentsByModule": enrollments_by_module,
            "enrollmentsByEstamento": enrollments_by_estamento,
            "enrollmentsByGrade": enrollments_by_grade,
            "recentEnrollments": recent_enrollments,
            "genderDistribution": gender_distribution,
            "estratoDistribution": estrato_distribution,
            "vinculacionDistribution": vinculacion_distribution,
            "municipioDistribution": municipio_distribution,
            "inscritosMatriculados": round(inscritosMatriculados, 2),
            "inscritosNoMatriculados": round(inscritosNoMatriculados, 2),
            "periodo_filtrado": periodo_id,
            "periodo_detalle": periodo_detalle,
            "filterOptions": {
                "modules": modulos_options,
                "areas": areas_options,
                "vinculaciones": vinculaciones_options,
                "estamentos": estamentos_options,
            }
        }

        return Response(payload)
    import sys
    @action(detail=False, methods=['get'], url_path="geocodificacion",
            permission_classes=[IsAdministrador])
    def geocodificacion(self, request):
        """
        Geocodifica la dirección de residencia de todos los estudiantes
        y retorna las coordenadas (Latitud, Longitud).
        """
        
        # 1. Inicializa el geocodificador (solo una vez)
        try:
            # Es crucial especificar un user_agent único y descriptivo
            geolocator = Nominatim(user_agent="semillero_estudiantes_v1")
        except GeocoderServiceError as e:
            return Response(
                {"error": f"Error al inicializar el geocodificador: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 2. Obtener los datos con Carga Ansiosa (Eager Loading)
        # ❗ Corrección: Usar select_related() para evitar N+1 consultas a la BD
        # Asume que 'id_estudiante' es el nombre de la relación ForeignKey
        try:
            inscripciones = self.get_queryset().select_related('id_estudiante')
        except Exception as e:
            return Response(
                {"error": f"Error al obtener las inscripciones: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        resultados = []
        
        # El print para debug ahora usa el queryset precargado
        if inscripciones.exists(): # Verifica que haya elementos antes de intentar acceder al índice
            print(inscripciones[0].id_estudiante.direccion_residencia, flush=True)

        # 3. Iterar y Geocodificar
        for inscripcion in inscripciones:
            # Acceso directo y eficiente al estudiante precargado
            estudiante = inscripcion.id_estudiante
            
            # Validar si el estudiante existe (aunque con select_related() ya debería estar precargado)
            if not estudiante:
                print(f"Advertencia: Inscripción con ID {inscripcion.pk} no tiene estudiante asociado.")
                continue
                
            # Construir la dirección completa para la geocodificación
            direccion_completa = (
                f"{estudiante.direccion_residencia}, "
                f"{estudiante.comuna_residencia}, "
                f"{estudiante.ciudad_residencia}, "
                f"{estudiante.departamento_residencia}"
            )

            latitud = None
            longitud = None
            location = None
            
            try:
                # Servicio de geocodificación. Usar timeout para evitar esperas largas.
                location = geolocator.geocode(direccion_completa, timeout=10)

                # Procesar el resultado
                if location:
                    latitud = location.latitude
                    longitud = location.longitude
                    
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                # Manejo de errores de red o del servicio de geocodificación
                print(f"Error geocodificando '{direccion_completa}': {e}")
                
            except Exception as e:
                # Otro error inesperado
                print(f"Error inesperado procesando '{direccion_completa}': {e}")
                
            # 4. Agregar el resultado a la lista de respuesta
            resultados.append({
                "id": estudiante.id_estudiante,
                "nombre_completo": f"{estudiante.nombre} {estudiante.apellido}", # Asumiendo campos
                "direccion_texto": direccion_completa,
                "latitud": latitud,
                "longitud": longitud,
                "encontrado": bool(location)
            })

        # 5. Retornar JSON al frontend
        return Response(resultados, status=status.HTTP_200_OK)

