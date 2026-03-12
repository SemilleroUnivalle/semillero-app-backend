from django.contrib import admin
from .models import EncuestaSatisfaccion


@admin.register(EncuestaSatisfaccion)
class EncuestaSatisfaccionAdmin(admin.ModelAdmin):
    list_display = (
        'id_encuesta',
        'get_documento',
        'get_nombre',
        'get_modulo',
        'get_docente',
        'get_monitor',
        'nota_modulo',
        'nota_docente',
        'nota_monitor',
        'nota_estudiante',
        'fecha_respuesta',
    )
    list_filter = ('fecha_respuesta', 'id_inscripcion__id_modulo')
    search_fields = (
        'id_inscripcion__id_estudiante__numero_documento',
        'id_inscripcion__id_estudiante__nombre',
        'id_inscripcion__id_estudiante__apellido',
    )
    readonly_fields = ('fecha_respuesta', 'fecha_ultimo_cambio')
    ordering = ('-fecha_respuesta',)

    # ── Columnas calculadas ───────────────────────────────────────────────
    @admin.display(description='Documento')
    def get_documento(self, obj):
        return obj.documento

    @admin.display(description='Nombre')
    def get_nombre(self, obj):
        return obj.nombre_completo

    @admin.display(description='Módulo')
    def get_modulo(self, obj):
        return obj.modulo

    @admin.display(description='Docente')
    def get_docente(self, obj):
        return obj.docente

    @admin.display(description='Monitor')
    def get_monitor(self, obj):
        return obj.monitor
