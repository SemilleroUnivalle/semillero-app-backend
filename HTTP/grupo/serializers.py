from rest_framework import serializers
from .models import Grupo

from profesor.serializers import ProfesorMeSerializer
from profesor.models import Profesor

from monitor_academico.serializers import MonitorAcademicoMeSerializer
from monitor_academico.models import MonitorAcademico

class GrupoSerializer(serializers.ModelSerializer):
    profesor = ProfesorMeSerializer(read_only=True)
    monitor_academico = MonitorAcademicoMeSerializer(read_only=True)

    class Meta:
        model = Grupo
        fields = '__all__'