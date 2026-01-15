from django.contrib import admin
from .models import PruebaDiagnostica, PreguntaDiagnostica, RespuestaDiagnostica


class RespuestaDiagnosticaInline(admin.TabularInline):
    """
    Inline para mostrar y editar respuestas dentro de la pregunta.
    """
    model = RespuestaDiagnostica
    extra = 1
    fields = ['texto_respuesta', 'es_correcta', 'fecha_creacion']
    readonly_fields = ['fecha_creacion']


class PreguntaDiagnosticaInline(admin.TabularInline):
    """
    Inline para mostrar preguntas dentro de la prueba.
    """
    model = PreguntaDiagnostica
    extra = 0
    fields = ['texto_pregunta', 'tipo_pregunta', 'puntaje', 'estado']
    show_change_link = True


@admin.register(PruebaDiagnostica)
class PruebaDiagnosticaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Pruebas Diagnósticas.
    """
    list_display = [
        'id_prueba', 'nombre_prueba', 'id_modulo', 
        'tiempo_limite', 'puntaje_minimo', 'estado', 
        'fecha_creacion'
    ]
    list_filter = ['estado', 'id_modulo', 'fecha_creacion']
    search_fields = ['nombre_prueba', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    inlines = [PreguntaDiagnosticaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_prueba', 'id_modulo', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('tiempo_limite', 'puntaje_minimo', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PreguntaDiagnostica)
class PreguntaDiagnosticaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Preguntas Diagnósticas.
    """
    list_display = [
        'id_pregunta', 'texto_pregunta_corto', 'id_prueba', 
        'tipo_pregunta', 'puntaje', 'estado'
    ]
    list_filter = ['tipo_pregunta', 'estado', 'id_prueba']
    search_fields = ['texto_pregunta']
    readonly_fields = ['fecha_creacion']
    inlines = [RespuestaDiagnosticaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id_prueba', 'texto_pregunta', 'tipo_pregunta')
        }),
        ('Configuración', {
            'fields': ('puntaje', 'imagen', 'explicacion', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def texto_pregunta_corto(self, obj):
        """Muestra solo los primeros 50 caracteres de la pregunta."""
        return obj.texto_pregunta[:50] + '...' if len(obj.texto_pregunta) > 50 else obj.texto_pregunta
    texto_pregunta_corto.short_description = 'Pregunta'


@admin.register(RespuestaDiagnostica)
class RespuestaDiagnosticaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Respuestas Diagnósticas.
    """
    list_display = [
        'id_respuesta', 'texto_respuesta_corto', 
        'id_pregunta', 'es_correcta', 'fecha_creacion'
    ]
    list_filter = ['es_correcta', 'id_pregunta']
    search_fields = ['texto_respuesta']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información', {
            'fields': ('id_pregunta', 'texto_respuesta', 'es_correcta')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def texto_respuesta_corto(self, obj):
        """Muestra solo los primeros 50 caracteres de la respuesta."""
        return obj.texto_respuesta[:50] + '...' if len(obj.texto_respuesta) > 50 else obj.texto_respuesta
    texto_respuesta_corto.short_description = 'Respuesta'
