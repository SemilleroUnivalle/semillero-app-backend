from rest_framework import serializers
from .models import MonitorAcademico
from modulo.models import Modulo
from modulo.serializers import ModuloProfesorSerializer
from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerMonitorAcademico

class MonitorAcademicoSerializer(serializers.ModelSerializer):
    audit_d10 = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_tabulado = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_estado_mat_financiera = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_documento_identidad = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_rut = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_certificado_bancario = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_foto = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_informacion = LogEntrySerializerMonitorAcademico(read_only=True)

    class Meta:
        model = MonitorAcademico
        fields = '__all__' 

class MonitorAcademicoModuloSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)
    audit_d10 = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_tabulado = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_estado_mat_financiera = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_documento_identidad = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_rut = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_certificado_bancario = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_foto = LogEntrySerializerMonitorAcademico(read_only=True)
    audit_informacion = LogEntrySerializerMonitorAcademico(read_only=True)

    class Meta:
        model = MonitorAcademico
        fields = '__all__' 

class AsignacionMonitorAcademicoSerializer(serializers.Serializer):
    id_monitor_academico = serializers.IntegerField()
    id_modulo = serializers.IntegerField()

    def validate(self, data):
        try:
            monitor_academico = MonitorAcademico.objects.get(id_monitor_academico=data['id_monitor_academico'])
        except MonitorAcademico.DoesNotExist:
            raise serializers.ValidationError("MonitorAcademico no encontrado")

        try:
            modulo = Modulo.objects.get(id_modulo=data['id_modulo'])
        except Modulo.DoesNotExist:
            raise serializers.ValidationError("Módulo no encontrado")

        return data

class MonitorAcademicoMeSerializer(serializers.Serializer):
    modulo = ModuloProfesorSerializer(read_only=True)

    class Meta:
        model = MonitorAcademico
        fields = ['id','nombre', 'apellido', 'numero_documento', 'email', 'ciudad_residencia', 'eps', 'tipo_documento', 'genero', 'fecha_nacimiento', 'telefono_fijo',
        'celular', 'departamento_residencia', 'comuna_residencia', 'direccion_residencia', 'foto', 'documento_identidad_pdf', 'rut_pdf', 'area_desempeño', 'semestre',
        'modulo', 'estado_mat_financiera_pdf', 'd10_pdf', 'tabulado_pdf']

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None