from rest_framework import serializers
from .models import MonitorAcademico
from modulo.models import Modulo
from modulo.serializers import ModuloProfesorSerializer

class MonitorAcademicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitorAcademico
        fields = '__all__' 

class MonitorAcademicoModuloSerializer(serializers.ModelSerializer):
    modulo = ModuloProfesorSerializer(read_only=True)

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