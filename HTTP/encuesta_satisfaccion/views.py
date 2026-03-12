from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Documentación Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Modelos
from .models import EncuestaSatisfaccion
from inscripcion.models import Inscripcion
from estudiante.models import Estudiante

# Serializers
from .serializers import EncuestaSatisfaccionSerializer, EncuestaSatisfaccionListSerializer

# Permisos
from cuenta.permissions import IsEstudiante, IsAdministrador, IsProfesor, IsProfesorOrAdministrador


class EncuestaSatisfaccionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar las encuestas de satisfacción.

    - Los **estudiantes** solo pueden crear/ver su propia encuesta.
    - Los **profesores** pueden ver las encuestas de los estudiantes de sus grupos.
    - Los **administradores** tienen acceso completo.

    Endpoints adicionales:
        GET  /encuesta_satisfaccion/encuesta/mis-encuestas/      → encuestas del estudiante autenticado
        GET  /encuesta_satisfaccion/encuesta/por-documento/{doc}/ → encuesta de un estudiante por documento
        GET  /encuesta_satisfaccion/encuesta/reporte/            → reporte completo (admin/profesor)
        POST /encuesta_satisfaccion/encuesta/cargar-excel/       → carga masiva desde archivo Excel
    """

    queryset = EncuestaSatisfaccion.objects.select_related(
        'id_inscripcion__id_estudiante',
        'id_inscripcion__id_modulo',
        'id_inscripcion__grupo__profesor',
    ).all()
    serializer_class = EncuestaSatisfaccionSerializer
    permission_classes = [IsAuthenticated]

    # ── Queryset dinámico según rol ────────────────────────────────────────
    def get_queryset(self):
        user = self.request.user
        qs = EncuestaSatisfaccion.objects.select_related(
            'id_inscripcion__id_estudiante',
            'id_inscripcion__id_modulo',
            'id_inscripcion__grupo__profesor',
        )

        if user.is_superuser or getattr(user, 'user_type', None) == 'administrador':
            return qs.all()

        if getattr(user, 'user_type', None) == 'profesor':
            from profesor.models import Profesor
            try:
                profesor = Profesor.objects.get(user=user)
                return qs.filter(id_inscripcion__grupo__profesor=profesor)
            except Profesor.DoesNotExist:
                return qs.none()

        if getattr(user, 'user_type', None) == 'estudiante':
            try:
                estudiante = Estudiante.objects.get(user=user)
                return qs.filter(id_inscripcion__id_estudiante=estudiante)
            except Estudiante.DoesNotExist:
                return qs.none()

        return qs.none()

    # ── Permisos por acción ────────────────────────────────────────────────
    def get_permissions(self):
        if self.action in ('create', 'mis_encuestas'):
            # Los estudiantes pueden crear y ver sus propias encuestas
            return [IsAuthenticated()]
        if self.action in ('list', 'retrieve', 'reporte', 'por_documento'):
            return [IsAuthenticated()]
        if self.action == 'cargar_excel':
            return [IsAuthenticated(), IsProfesorOrAdministrador()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAdministrador()]
        return [IsAuthenticated()]

    # ── Serializer según acción ───────────────────────────────────────────
    def get_serializer_class(self):
        if self.action in ('list', 'reporte', 'mis_encuestas'):
            return EncuestaSatisfaccionListSerializer
        return EncuestaSatisfaccionSerializer

    # ── Crear o actualizar (upsert) ───────────────────────────────────────
    @swagger_auto_schema(
        operation_summary='Crear o actualizar encuesta de satisfacción',
        operation_description=(
            'Si ya existe una encuesta para la inscripción indicada se actualiza; '
            'si no, se crea una nueva. El estudiante solo puede responder su propia encuesta.'
        ),
        request_body=EncuestaSatisfaccionSerializer,
        responses={
            201: EncuestaSatisfaccionSerializer,
            200: EncuestaSatisfaccionSerializer,
            400: 'Datos inválidos',
            403: 'Sin permiso',
        },
    )
    def create(self, request, *args, **kwargs):
        id_inscripcion = request.data.get('id_inscripcion')

        if not id_inscripcion:
            return Response(
                {'error': 'El campo id_inscripcion es requerido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar que el estudiante solo responda su propia encuesta
        user = request.user
        if getattr(user, 'user_type', None) == 'estudiante':
            try:
                estudiante = Estudiante.objects.get(user=user)
                if not Inscripcion.objects.filter(
                    id_inscripcion=id_inscripcion,
                    id_estudiante=estudiante,
                ).exists():
                    return Response(
                        {'error': 'No tienes permiso para responder esta encuesta.'},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except Estudiante.DoesNotExist:
                return Response(
                    {'error': 'No se encontró perfil de estudiante.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Upsert
        encuesta = EncuestaSatisfaccion.objects.filter(id_inscripcion=id_inscripcion).first()

        if encuesta:
            data = request.data.copy()
            data.pop('id_inscripcion', None)
            serializer = self.get_serializer(encuesta, data=data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        http_status = status.HTTP_200_OK if encuesta else status.HTTP_201_CREATED
        return Response(serializer.data, status=http_status)

    # ── Acción: carga masiva desde Excel ─────────────────────────────────
    @swagger_auto_schema(
        operation_summary='Carga masiva de encuestas desde archivo Excel',
        operation_description=(
            'Recibe un archivo Excel (.xlsx o .xls) con las columnas:\n\n'
            '`documento`, `nombre`, `modulo`, `docente`, `monitor`, '
            '`nota_modulo`, `nota_docente`, `nota_monitor`, `nota_estudiante`\n\n'
            'El backend busca al estudiante por `documento` (numero_documento), '
            'obtiene su inscripción más reciente y hace un upsert de la encuesta.\n\n'
            'Las columnas `nombre`, `modulo`, `docente` y `monitor` son informativas '
            'y no se persisten (quedan calculadas automáticamente desde el modelo).\n\n'
            'Devuelve un reporte con las filas creadas, actualizadas y los errores.'
        ),
        manual_parameters=[
            openapi.Parameter(
                name='archivo',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Archivo Excel (.xlsx / .xls) con la estructura de encuesta',
            )
        ],
        responses={
            200: openapi.Response(
                description='Resultado de la carga masiva',
                examples={
                    'application/json': {
                        'mensaje': 'Carga finalizada.',
                        'total_filas': 10,
                        'creadas': 7,
                        'actualizadas': 2,
                        'errores': 1,
                        'detalle_errores': [
                            {
                                'fila': 5,
                                'documento': '9999999',
                                'error': 'Estudiante no encontrado en el sistema.',
                            }
                        ],
                        'detalle_exito': [
                            {
                                'fila': 1,
                                'documento': '1001234567',
                                'nombre': 'Juan Perez',
                                'id_inscripcion': 42,
                                'id_encuesta': 13,
                                'accion': 'creada',
                                'notas_guardadas': {
                                    'nota_modulo': '4.5',
                                    'nota_docente': '4.7',
                                },
                            }
                        ],
                    }
                },
            ),
            400: 'No se envió archivo o el formato es incorrecto',
        },
    )
    @action(
        detail=False,
        methods=['post'],
        url_path='cargar-excel',
        permission_classes=[IsAuthenticated, IsProfesorOrAdministrador],
    )
    def cargar_excel(self, request):
        """
        Carga masiva de encuestas de satisfacción desde un archivo Excel.

        Columnas requeridas : documento
        Columnas de notas   : nota_modulo, nota_docente, nota_monitor, nota_estudiante
                              (al menos una por fila, escala 0.0 – 5.0)
        Columnas opcionales : nombre, modulo, docente, monitor, comentarios
                              (informativas; nombre/modulo/docente/monitor se ignoran al persistir)
        """
        import pandas as pd
        from decimal import Decimal, InvalidOperation

        # ── 1. Validar archivo ────────────────────────────────────────────
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response(
                {'error': 'Debes enviar un archivo Excel en el campo "archivo".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        nombre_archivo = archivo.name.lower()
        if not (nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls')):
            return Response(
                {'error': 'El archivo debe ser .xlsx o .xls.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── 2. Leer con pandas ────────────────────────────────────────────
        try:
            # dtype=str para que pandas no convierta documentos a float (ej: 1001234567.0)
            df = pd.read_excel(archivo, dtype=str)
        except Exception as exc:
            return Response(
                {'error': f'No se pudo leer el archivo Excel: {str(exc)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Normalizar nombres de columna
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]

        # ── 3. Validar estructura mínima ──────────────────────────────────
        if 'documento' not in df.columns:
            return Response(
                {
                    'error': 'El archivo no contiene la columna "documento".',
                    'columnas_encontradas': list(df.columns),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        COLUMNAS_NOTAS = ['nota_modulo', 'nota_docente', 'nota_monitor', 'nota_estudiante']
        columnas_notas_presentes = [c for c in COLUMNAS_NOTAS if c in df.columns]

        if not columnas_notas_presentes:
            return Response(
                {
                    'error': (
                        'El archivo no contiene ninguna columna de notas. '
                        'Se esperan: nota_modulo, nota_docente, nota_monitor, nota_estudiante.'
                    ),
                    'columnas_encontradas': list(df.columns),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── Helper: convertir celda a Decimal validado ────────────────────
        def parse_nota(valor):
            if valor is None:
                return None
            s = str(valor).strip().replace(',', '.')
            if s in ('', 'nan', 'none', 'NaN', 'None', '-'):
                return None
            try:
                d = Decimal(s)
            except InvalidOperation:
                raise ValueError(f'"{s}" no es un número válido.')
            if d < Decimal('0') or d > Decimal('5'):
                raise ValueError(f'Nota {d} fuera del rango permitido (0.0 – 5.0).')
            return d

        # ── 4. Procesar fila a fila ───────────────────────────────────────
        creadas = 0
        actualizadas = 0
        detalle_errores = []
        detalle_exito = []

        for idx, row in df.iterrows():
            fila_num = idx + 2  # fila 1 = encabezado → datos desde fila 2

            # 4a. Documento
            documento = str(row.get('documento', '')).strip()
            # pandas puede leer "1001234567.0" si la celda era numérica
            if '.' in documento:
                documento = documento.split('.')[0]

            if not documento or documento in ('nan', 'None', ''):
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': 'El campo "documento" está vacío.',
                })
                continue

            # 4b. Buscar estudiante por número de documento
            try:
                estudiante = Estudiante.objects.get(numero_documento=documento)
            except Estudiante.DoesNotExist:
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': 'Estudiante no encontrado en el sistema.',
                })
                continue

            # 4c. Obtener la inscripción más reciente del estudiante
            inscripcion = (
                Inscripcion.objects
                .filter(id_estudiante=estudiante)
                .order_by('-fecha_inscripcion')
                .first()
            )
            if not inscripcion:
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': 'El estudiante no tiene ninguna inscripción registrada.',
                })
                continue

            # 4d. Parsear notas
            notas = {}
            error_nota = None
            for campo in columnas_notas_presentes:
                try:
                    notas[campo] = parse_nota(row.get(campo))
                except ValueError as exc:
                    error_nota = f'Columna "{campo}": {exc}'
                    break

            if error_nota:
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': error_nota,
                })
                continue

            # Verificar que al menos una nota tenga valor
            if all(v is None for v in notas.values()):
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': 'La fila no contiene ninguna nota válida.',
                })
                continue

            # 4e. Campo opcional: comentarios
            comentarios = None
            if 'comentarios' in df.columns:
                val = str(row.get('comentarios', '')).strip()
                if val not in ('', 'nan', 'None'):
                    comentarios = val

            # 4f. Upsert
            try:
                encuesta, creada = EncuestaSatisfaccion.objects.get_or_create(
                    id_inscripcion=inscripcion,
                )

                # Solo actualizar campos que traigan valor en el Excel
                for campo, valor in notas.items():
                    if valor is not None:
                        setattr(encuesta, campo, valor)

                if comentarios is not None:
                    encuesta.comentarios = comentarios

                encuesta.save()

                if creada:
                    creadas += 1
                else:
                    actualizadas += 1

                detalle_exito.append({
                    'fila': fila_num,
                    'documento': documento,
                    'nombre': f"{estudiante.nombre} {estudiante.apellido}",
                    'id_inscripcion': inscripcion.id_inscripcion,
                    'id_encuesta': encuesta.id_encuesta,
                    'accion': 'creada' if creada else 'actualizada',
                    'notas_guardadas': {k: str(v) for k, v in notas.items() if v is not None},
                })

            except Exception as exc:
                detalle_errores.append({
                    'fila': fila_num,
                    'documento': documento,
                    'error': f'Error al guardar en base de datos: {str(exc)}',
                })

        # ── 5. Respuesta resumen ──────────────────────────────────────────
        return Response(
            {
                'mensaje': 'Carga finalizada.',
                'total_filas': len(df),
                'creadas': creadas,
                'actualizadas': actualizadas,
                'errores': len(detalle_errores),
                'detalle_exito': detalle_exito,
                'detalle_errores': detalle_errores,
            },
            status=status.HTTP_200_OK,
        )

    # ── Acción: encuestas del estudiante autenticado ──────────────────────
    @swagger_auto_schema(
        operation_summary='Mis encuestas de satisfacción',
        operation_description='Retorna las encuestas respondidas por el estudiante autenticado.',
        responses={200: EncuestaSatisfaccionListSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='mis-encuestas')
    def mis_encuestas(self, request):
        user = request.user
        if getattr(user, 'user_type', None) != 'estudiante':
            return Response(
                {'error': 'Solo los estudiantes pueden acceder a este endpoint.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            estudiante = Estudiante.objects.get(user=user)
        except Estudiante.DoesNotExist:
            return Response(
                {'error': 'No se encontró perfil de estudiante.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        encuestas = EncuestaSatisfaccion.objects.select_related(
            'id_inscripcion__id_estudiante',
            'id_inscripcion__id_modulo',
            'id_inscripcion__grupo__profesor',
        ).filter(id_inscripcion__id_estudiante=estudiante)

        serializer = EncuestaSatisfaccionListSerializer(encuestas, many=True)
        return Response(serializer.data)

    # ── Acción: buscar encuesta por número de documento ───────────────────
    @swagger_auto_schema(
        operation_summary='Encuesta por número de documento del estudiante',
        operation_description=(
            'Retorna todas las encuestas de satisfacción de un estudiante '
            'identificado por su número de documento.'
        ),
        manual_parameters=[
            openapi.Parameter(
                'documento',
                openapi.IN_PATH,
                description='Número de documento del estudiante',
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: EncuestaSatisfaccionListSerializer(many=True),
            404: 'Estudiante no encontrado',
        },
    )
    @action(
        detail=False,
        methods=['get'],
        url_path=r'por-documento/(?P<documento>[^/.]+)',
        permission_classes=[IsAuthenticated, IsProfesorOrAdministrador],
    )
    def por_documento(self, request, documento=None):
        try:
            estudiante = Estudiante.objects.get(numero_documento=documento)
        except Estudiante.DoesNotExist:
            return Response(
                {'error': f'No se encontró ningún estudiante con documento {documento}.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        encuestas = EncuestaSatisfaccion.objects.select_related(
            'id_inscripcion__id_estudiante',
            'id_inscripcion__id_modulo',
            'id_inscripcion__grupo__profesor',
        ).filter(id_inscripcion__id_estudiante=estudiante)

        serializer = EncuestaSatisfaccionListSerializer(encuestas, many=True)
        return Response(serializer.data)

    # ── Acción: reporte completo (tabla de la imagen) ────────────────────
    @swagger_auto_schema(
        operation_summary='Reporte de encuestas de satisfacción',
        operation_description=(
            'Retorna un listado completo (formato tabla) con documento, nombre, '
            'módulo, docente, monitor y las cuatro notas para cada estudiante. '
            'Los profesores ven solo sus grupos; los administradores ven todo.'
        ),
        responses={200: EncuestaSatisfaccionListSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=['get'],
        url_path='reporte',
        permission_classes=[IsAuthenticated, IsProfesorOrAdministrador],
    )
    def reporte(self, request):
        encuestas = self.get_queryset()
        serializer = EncuestaSatisfaccionListSerializer(encuestas, many=True)
        return Response(serializer.data)
