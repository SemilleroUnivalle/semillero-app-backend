from rest_framework import serializers
from .models import MonitorAdministrativo
from auditlog.models import LogEntry
from .auditlog_serializer import LogEntrySerializerMonitorAdministrativo

class MonitorAdministrativoSerializer(serializers.ModelSerializer):
    audit_d10 = LogEntrySerializerMonitorAdministrativo(read_only=True)
    audit_tabulado = LogEntrySerializerMonitorAdministrativo(read_only=True)
    audit_estado_mat_financiera = LogEntrySerializerMonitorAdministrativo(read_only=True)
    audit_documento_identidad = LogEntrySerializerMonitorAdministrativo(read_only=True)
    audit_rut = LogEntrySerializerMonitorAdministrativo(read_only=True)
    audit_certificado_bancario = LogEntrySerializerMonitorAdministrativo(read_only=True)
    class Meta:
        model = MonitorAdministrativo
        fields = '__all__' 

class LogEntrySerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_usuario(self, obj):
        return obj.actor.username if obj.actor else None