from rest_framework import serializers
from .models import Inscripcion

from modulo.serializers import ModuloReadSerializer
from modulo.models import Modulo

from estudiante.serializers import EstudianteSerializerMatricula
from estudiante.models import Estudiante

from oferta_categoria.serializers import OfertaCategoriaInscripcionReadSerializer
from oferta_categoria.models import OfertaCategoria

from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerEstudiante

from profesor.serializers import ProfesorSimpleSerializer

class InscripcionSerializer(serializers.ModelSerializer):
    id_modulo = serializers.PrimaryKeyRelatedField(queryset=Modulo.objects.all(), write_only=True)
    modulo = ModuloReadSerializer(source='id_modulo', read_only=True)

    id_estudiante = serializers.PrimaryKeyRelatedField(queryset=Estudiante.objects.all(), write_only=True)
    estudiante = EstudianteSerializerMatricula(source='id_estudiante', read_only=True)

    id_oferta_categoria = serializers.PrimaryKeyRelatedField(queryset=OfertaCategoria.objects.all(), write_only=True)
    oferta_categoria = OfertaCategoriaInscripcionReadSerializer(source='id_oferta_categoria', read_only=True)

    audit_documento_recibo_pago = LogEntrySerializerEstudiante(read_only=True)
    audit_certificado = LogEntrySerializerEstudiante(read_only=True)


    class Meta:
        model = Inscripcion
        fields = ['id_inscripcion', 'id_estudiante','estudiante', 'id_modulo','modulo', 'id_oferta_categoria','oferta_categoria', 'grupo', 'fecha_inscripcion', 'tipo_vinculacion', 
        'terminos', 'observaciones', 'audit_certificado', 'audit_documento_recibo_pago']
        read_only_fields = ('id_inscripcion',)
        

class InscripcionInfProfeSerializer(serializers.ModelSerializer):
    id_modulo = serializers.PrimaryKeyRelatedField(queryset=Modulo.objects.all(), write_only=True)
    modulo = ModuloReadSerializer(source='id_modulo', read_only=True)

    id_estudiante = serializers.PrimaryKeyRelatedField(queryset=Estudiante.objects.all(), write_only=True)
    estudiante = EstudianteSerializerMatricula(source='id_estudiante', read_only=True)

    id_oferta_categoria = serializers.PrimaryKeyRelatedField(queryset=OfertaCategoria.objects.all(), write_only=True)
    oferta_categoria = OfertaCategoriaInscripcionReadSerializer(source='id_oferta_categoria', read_only=True)

    audit_documento_recibo_pago = LogEntrySerializerEstudiante(read_only=True)
    audit_certificado = LogEntrySerializerEstudiante(read_only=True)

    profesor = serializers.SerializerMethodField()

    class Meta:
        model = Inscripcion
        fields = ['profesor','id_inscripcion', 'id_estudiante','estudiante', 'id_modulo','modulo', 'id_oferta_categoria','oferta_categoria', 'grupo', 'fecha_inscripcion', 'tipo_vinculacion', 
        'terminos', 'observaciones', 'audit_certificado', 'audit_documento_recibo_pago']
        read_only_fields = ('id_inscripcion',)
        

    def get_profesor(self, obj):
        if obj.grupo:
            profesor_instance = obj.grupo.profesor

            if profesor_instance:
                return ProfesorSimpleSerializer(profesor_instance).data

        return None

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None