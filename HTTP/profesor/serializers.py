from rest_framework import serializers
from .models import Profesor
from modulo.models import Modulo
from modulo.serializers import ModuloProfesorSerializer
from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerProfesor

class ProfesorSerializer(serializers.ModelSerializer):
    audit_hoja_vida = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_laboral = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_academico = LogEntrySerializerProfesor(read_only=True)
    audit_documento_identidad = LogEntrySerializerProfesor(read_only=True)
    audit_rut = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_bancario = LogEntrySerializerProfesor(read_only=True)
    audit_foto = LogEntrySerializerProfesor(read_only=True)
    audit_informacion = LogEntrySerializerProfesor(read_only=True)

    class Meta:
        model = Profesor
        fields = '__all__' 

class ProfesorModuloSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)
    audit_hoja_vida = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_laboral = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_academico = LogEntrySerializerProfesor(read_only=True)
    audit_documento_identidad = LogEntrySerializerProfesor(read_only=True)
    audit_rut = LogEntrySerializerProfesor(read_only=True)
    audit_certificado_bancario = LogEntrySerializerProfesor(read_only=True)
    audit_foto = LogEntrySerializerProfesor(read_only=True)
    audit_informacion = LogEntrySerializerProfesor(read_only=True)

    class Meta:
        model = Profesor
        fields = '__all__' 

class AsignacionProfesorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    id_modulo = serializers.IntegerField()

    def validate(self, data):
        try:
            profesor = Profesor.objects.get(id=data['id'])
        except Profesor.DoesNotExist:
            raise serializers.ValidationError("Profesor no encontrado")

        try:
            modulo = Modulo.objects.get(id_modulo=data['id_modulo'])
        except Modulo.DoesNotExist:
            raise serializers.ValidationError("Módulo no encontrado")

        return data

class ProfesorMeSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)

    class Meta:
        model = Profesor
        fields = ['id','nombre', 'apellido', 'numero_documento', 'email', 'ciudad_residencia', 'eps', 'tipo_documento', 'genero', 'fecha_nacimiento', 'telefono_fijo',
        'celular', 'departamento_residencia', 'comuna_residencia', 'direccion_residencia', 'foto', 'documento_identidad_pdf', 'rut_pdf', 'certificado_laboral_pdf',
        'certificado_bancario_pdf', 'area_desempeño', 'grado_escolaridad', 'hoja_vida_pdf', 'certificado_academico_pdf', 'modulo']

class ProfesorSimpleSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)

    class Meta:
        model = Profesor
        fields = ['id','nombre', 'apellido', 'numero_documento', 'email', 'celular', 'foto', 'area_desempeño', 'grado_escolaridad', 'modulo']

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None