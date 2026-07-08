from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class EncuestaSatisfaccion(models.Model):
    """
    Encuesta de satisfacción vinculada a cada estudiante mediante su
    inscripción. Recoge la valoración que el estudiante hace del módulo,
    del docente, del monitor y su propia autoevaluación.

    Campos que se exponen:
        documento        → numero_documento del estudiante (via inscripción)
        nombre           → nombre + apellido del estudiante (via inscripción)
        modulo           → nombre del módulo (via inscripción)
        docente          → nombre del profesor del grupo
        monitor          → nombre del monitor académico del módulo
        nota_modulo      → calificación que el estudiante da al módulo   (0.0 – 5.0)
        nota_docente     → calificación al docente                        (0.0 – 5.0)
        nota_monitor     → calificación al monitor                        (0.0 – 5.0)
        nota_estudiante  → autoevaluación del estudiante                  (0.0 – 5.0)
    """

    NOTA_VALIDATORS = [
        MinValueValidator(Decimal('0.0')),
        MaxValueValidator(Decimal('5.0')),
    ]

    id_encuesta = models.AutoField(primary_key=True)

    # Relación principal: una inscripción → una única encuesta de satisfacción
    id_inscripcion = models.OneToOneField(
        'inscripcion.Inscripcion',
        on_delete=models.CASCADE,
        related_name='encuesta_satisfaccion',
        verbose_name='Inscripción',
    )

    # ── Calificaciones (escala 0.0 – 5.0, dos decimales) ──────────────────
    nota_modulo = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=NOTA_VALIDATORS,
        null=True,
        blank=True,
        verbose_name='Nota al módulo',
        help_text='Calificación del estudiante al contenido del módulo (0.0 – 5.0)',
    )
    nota_docente = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=NOTA_VALIDATORS,
        null=True,
        blank=True,
        verbose_name='Nota al docente',
        help_text='Calificación del estudiante al desempeño del docente (0.0 – 5.0)',
    )
    nota_monitor = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=NOTA_VALIDATORS,
        null=True,
        blank=True,
        verbose_name='Nota al monitor',
        help_text='Calificación del estudiante al desempeño del monitor (0.0 – 5.0)',
    )
    nota_estudiante = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=NOTA_VALIDATORS,
        null=True,
        blank=True,
        verbose_name='Autoevaluación del estudiante',
        help_text='Autoevaluación del estudiante (0.0 – 5.0)',
    )

    # ── Campos auxiliares ─────────────────────────────────────────────────
    comentarios = models.TextField(
        blank=True,
        null=True,
        verbose_name='Comentarios',
        help_text='Observaciones o sugerencias del estudiante',
    )
    fecha_respuesta = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de respuesta',
    )
    fecha_ultimo_cambio = models.DateTimeField(
        auto_now=True,
        verbose_name='Última modificación',
    )

    # ── Propiedades de solo lectura calculadas ────────────────────────────
    @property
    def documento(self):
        """Número de documento del estudiante."""
        return self.id_inscripcion.id_estudiante.numero_documento

    @property
    def nombre_completo(self):
        """Nombre completo del estudiante."""
        est = self.id_inscripcion.id_estudiante
        return f"{est.nombre} {est.apellido}"

    @property
    def modulo(self):
        """Nombre del módulo en el que está inscrito el estudiante."""
        modulo = self.id_inscripcion.id_modulo
        return modulo.nombre_modulo if modulo else 'N/A'

    @property
    def docente(self):
        """Nombre del docente/profesor asignado al grupo."""
        grupo = self.id_inscripcion.grupo
        if grupo and grupo.profesor:
            p = grupo.profesor
            return f"{p.nombre} {p.apellido}"
        return 'N/A'

    @property
    def monitor(self):
        """Nombre del monitor académico vinculado al módulo."""
        modulo = self.id_inscripcion.id_modulo
        if modulo:
            monitor_qs = modulo.monitor_academico.first()
            if monitor_qs:
                return f"{monitor_qs.nombre} {monitor_qs.apellido}"
        return 'N/A'

    def __str__(self):
        return (
            f"Encuesta #{self.id_encuesta} – "
            f"{self.nombre_completo} (Doc: {self.documento})"
        )

    class Meta:
        verbose_name = 'Encuesta de Satisfacción'
        verbose_name_plural = 'Encuestas de Satisfacción'
        ordering = ['-fecha_respuesta']
