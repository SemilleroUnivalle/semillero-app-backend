from rest_framework import serializers
from auditlog.models import LogEntry

class LogEntrySerializerEstudiante(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = '__all__' 