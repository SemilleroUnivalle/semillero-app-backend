from django.db import models
from django.core.exceptions import ValidationError
from modulo.models import Modulo


class PruebaDiagnostica(models.Model):
    """
    Modelo para agrupar un conjunto de preguntas diagnósticas por módulo.
    Esto permite crear diferentes versiones de pruebas para el mismo módulo.
    """
    id_prueba = models.AutoField(primary_key=True)
    id_modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='pruebas_diagnosticas',
        verbose_name='Módulo'
    )
    nombre_prueba = models.CharField(max_length=200, verbose_name='Nombre de la Prueba')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    tiempo_limite = models.PositiveIntegerField(
        default=60,
        help_text='Tiempo límite en minutos',
        verbose_name='Tiempo Límite (min)'
    )
    puntaje_minimo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=60.00,
        help_text='Puntaje mínimo para aprobar (%)',
        verbose_name='Puntaje Mínimo (%)'
    )
    estado = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Última Modificación')

    def __str__(self):
        return f"{self.nombre_prueba} - {self.id_modulo.nombre_modulo}"

    class Meta:
        verbose_name = 'Prueba Diagnóstica'
        verbose_name_plural = 'Pruebas Diagnósticas'
        ordering = ['-fecha_creacion']

class PreguntaDiagnostica(models.Model):
    """
    Modelo para las preguntas de la prueba diagnóstica.
    """
    TIPO_PREGUNTA_CHOICES = [
        ('multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
    ]

    id_pregunta = models.AutoField(primary_key=True)
    id_prueba = models.ForeignKey(
        PruebaDiagnostica,
        on_delete=models.CASCADE,
        related_name='preguntas',
        verbose_name='Prueba Diagnóstica'
    )
    texto_pregunta = models.TextField(verbose_name='Pregunta')
    tipo_pregunta = models.CharField(
        max_length=20,
        choices=TIPO_PREGUNTA_CHOICES,
        default='multiple',
        verbose_name='Tipo de Pregunta'
    )
    puntaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        verbose_name='Puntaje'
    )
    imagen = models.ImageField(
        upload_to='preguntas_diagnosticas/',
        blank=True,
        null=True,
        verbose_name='Imagen'
    )
    explicacion = models.TextField(
        blank=True,
        null=True,
        help_text='Explicación de la respuesta correcta',
        verbose_name='Explicación'
    )
    estado = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Última Modificación')

    def __str__(self):
        return f" {self.texto_pregunta[:50]}..."

    class Meta:
        verbose_name = 'Pregunta Diagnóstica'
        verbose_name_plural = 'Preguntas Diagnósticas'
        ordering = ['id_prueba', 'fecha_creacion']
        unique_together = ['id_prueba', 'fecha_creacion']


class RespuestaDiagnostica(models.Model):
    """
    Modelo para las opciones de respuesta de cada pregunta.
    Solo una respuesta puede ser correcta por pregunta.
    """
    id_respuesta = models.AutoField(primary_key=True)
    id_pregunta = models.ForeignKey(
        PreguntaDiagnostica,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Pregunta'
    )
    texto_respuesta = models.TextField(verbose_name='Respuesta')
    es_correcta = models.BooleanField(default=False, verbose_name='¿Es Correcta?')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def clean(self):
        """
        Validación para asegurar que solo haya una respuesta correcta por pregunta.
        """
        if self.es_correcta:
            # Verificar si ya existe otra respuesta correcta para esta pregunta
            respuestas_correctas = RespuestaDiagnostica.objects.filter(
                id_pregunta=self.id_pregunta,
                es_correcta=True
            ).exclude(id_respuesta=self.id_respuesta)
            
            if respuestas_correctas.exists():
                raise ValidationError(
                    'Ya existe una respuesta correcta para esta pregunta. '
                    'Solo puede haber una respuesta correcta por pregunta.'
                )

    def save(self, *args, **kwargs):
        """
        Sobrescribir save para ejecutar la validación.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        correcta = "✓" if self.es_correcta else "✗"
        return f"{correcta} {self.texto_respuesta[:50]}..."

    class Meta:
        verbose_name = 'Respuesta Diagnóstica'
        verbose_name_plural = 'Respuestas Diagnósticas'
        ordering = ['id_pregunta', 'fecha_creacion']
        unique_together = ['id_pregunta', 'fecha_creacion']
