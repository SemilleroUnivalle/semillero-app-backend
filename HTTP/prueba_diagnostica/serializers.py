from rest_framework import serializers
from .models import PruebaDiagnostica, PreguntaDiagnostica, RespuestaDiagnostica
from modulo.serializers import ModuloReadSerializer


class RespuestaDiagnosticaSerializer(serializers.ModelSerializer):
    """
    Serializer para las respuestas de las preguntas diagnósticas.
    """
    class Meta:
        model = RespuestaDiagnostica
        fields = ['id_respuesta', 'texto_respuesta', 'es_correcta', 'fecha_creacion']
        read_only_fields = ['id_respuesta', 'fecha_creacion']


class RespuestaDiagnosticaWriteSerializer(serializers.ModelSerializer):
    """
    Serializer para crear/actualizar respuestas (sin mostrar si es correcta en la respuesta pública).
    """
    class Meta:
        model = RespuestaDiagnostica
        fields = ['id_respuesta', 'id_pregunta', 'texto_respuesta', 'es_correcta', 'fecha_creacion']
        read_only_fields = ['id_respuesta', 'fecha_creacion']


class PreguntaDiagnosticaReadSerializer(serializers.ModelSerializer):
    """
    Serializer para leer preguntas con sus respuestas.
    """
    respuestas = RespuestaDiagnosticaSerializer(many=True, read_only=True)
    
    class Meta:
        model = PreguntaDiagnostica
        fields = [
            'id_pregunta', 'texto_pregunta', 'tipo_pregunta', 
            'puntaje', 'imagen', 'explicacion', 
            'estado', 'fecha_creacion', 'respuestas'
        ]
        read_only_fields = ['id_pregunta', 'fecha_creacion']


class PreguntaDiagnosticaWriteSerializer(serializers.ModelSerializer):
    """
    Serializer para crear/actualizar preguntas.
    """
    class Meta:
        model = PreguntaDiagnostica
        fields = [
            'id_pregunta', 'id_prueba', 'texto_pregunta', 
            'tipo_pregunta', 'puntaje', 'imagen', 
            'explicacion', 'estado', 'fecha_creacion'
        ]
        read_only_fields = ['id_pregunta', 'fecha_creacion']


class PruebaDiagnosticaReadSerializer(serializers.ModelSerializer):
    """
    Serializer para leer pruebas diagnósticas con sus preguntas.
    """
    id_modulo = ModuloReadSerializer(read_only=True)
    preguntas = PreguntaDiagnosticaReadSerializer(many=True, read_only=True)
    total_preguntas = serializers.SerializerMethodField()
    
    class Meta:
        model = PruebaDiagnostica
        fields = [
            'id_prueba', 'id_modulo', 'nombre_prueba', 'descripcion',
            'tiempo_limite', 'puntaje_minimo', 'estado', 
            'fecha_creacion', 'fecha_modificacion', 'preguntas',
            'total_preguntas'
        ]
        read_only_fields = ['id_prueba', 'fecha_creacion', 'fecha_modificacion']
    
    def get_total_preguntas(self, obj):
        """Retorna el número total de preguntas en la prueba."""
        return obj.preguntas.filter(estado=True).count()


class PruebaDiagnosticaWriteSerializer(serializers.ModelSerializer):
    """
    Serializer para crear/actualizar pruebas diagnósticas.
    """
    class Meta:
        model = PruebaDiagnostica
        fields = [
            'id_prueba', 'id_modulo', 'nombre_prueba', 'descripcion',
            'tiempo_limite', 'puntaje_minimo', 'estado'
        ]
        read_only_fields = ['id_prueba']


class PreguntaConRespuestasSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una pregunta junto con sus respuestas en una sola operación.
    """
    respuestas = RespuestaDiagnosticaWriteSerializer(many=True)
    
    class Meta:
        model = PreguntaDiagnostica
        fields = [
            'id_pregunta', 'id_prueba', 'texto_pregunta', 
            'tipo_pregunta', 'puntaje', 'imagen', 
            'explicacion', 'estado', 'respuestas'
        ]
        read_only_fields = ['id_pregunta']
    
    def create(self, validated_data):
        """
        Crea la pregunta y sus respuestas en una transacción.
        """
        respuestas_data = validated_data.pop('respuestas')
        pregunta = PreguntaDiagnostica.objects.create(**validated_data)
        
        for respuesta_data in respuestas_data:
            RespuestaDiagnostica.objects.create(
                id_pregunta=pregunta,
                **respuesta_data
            )
        
        return pregunta
    
    def update(self, instance, validated_data):
        """
        Actualiza la pregunta y opcionalmente sus respuestas.
        """
        respuestas_data = validated_data.pop('respuestas', None)
        
        # Actualizar campos de la pregunta
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Si se proporcionan respuestas, actualizar o crear
        if respuestas_data is not None:
            # Eliminar respuestas antiguas y crear nuevas
            instance.respuestas.all().delete()
            for respuesta_data in respuestas_data:
                RespuestaDiagnostica.objects.create(
                    id_pregunta=instance,
                    **respuesta_data
                )
        
        return instance
