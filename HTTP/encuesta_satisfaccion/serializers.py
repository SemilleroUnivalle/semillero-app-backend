from rest_framework import serializers
from .models import EncuestaSatisfaccion


class EncuestaSatisfaccionSerializer(serializers.ModelSerializer):
    """
    Serializer para EncuestaSatisfaccion.

    Expone todos los campos del modelo más los campos calculados
    (propiedades de solo lectura) que corresponden a los datos
    visibles en la tabla de la imagen:
        documento, nombre, modulo, docente, monitor
    """

    # ── Campos calculados (solo lectura) ──────────────────────────────────
    documento = serializers.ReadOnlyField()
    nombre = serializers.ReadOnlyField(source='nombre_completo')
    modulo = serializers.ReadOnlyField()
    docente = serializers.ReadOnlyField()
    monitor = serializers.ReadOnlyField()

    class Meta:
        model = EncuestaSatisfaccion
        fields = [
            # Clave primaria y FK de escritura
            'id_encuesta',
            'id_inscripcion',

            # Campos informativos (solo lectura)
            'documento',
            'nombre',
            'modulo',
            'docente',
            'monitor',

            # Calificaciones escritas por el estudiante
            'nota_modulo',
            'nota_docente',
            'nota_monitor',
            'nota_estudiante',

            # Metadata
            'comentarios',
            'fecha_respuesta',
            'fecha_ultimo_cambio',
        ]
        read_only_fields = (
            'id_encuesta',
            'fecha_respuesta',
            'fecha_ultimo_cambio',
        )

    def validate(self, data):
        """Valida que al menos una nota haya sido proporcionada."""
        notas = [
            data.get('nota_modulo'),
            data.get('nota_docente'),
            data.get('nota_monitor'),
            data.get('nota_estudiante'),
        ]
        if all(n is None for n in notas):
            raise serializers.ValidationError(
                'Debe proporcionar al menos una nota (módulo, docente, monitor o autoevaluación).'
            )
        return data


class EncuestaSatisfaccionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listados (vista tabla de la imagen).
    Muestra todos los campos requeridos en la imagen en un formato plano.
    """
    documento = serializers.ReadOnlyField()
    nombre = serializers.ReadOnlyField(source='nombre_completo')
    modulo = serializers.ReadOnlyField()
    docente = serializers.ReadOnlyField()
    monitor = serializers.ReadOnlyField()

    class Meta:
        model = EncuestaSatisfaccion
        fields = [
            'id_encuesta',
            'documento',
            'nombre',
            'modulo',
            'docente',
            'monitor',
            'nota_modulo',
            'nota_docente',
            'nota_monitor',
            'nota_estudiante',
            'fecha_respuesta',
        ]
