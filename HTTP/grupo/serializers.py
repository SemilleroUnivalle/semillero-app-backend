from rest_framework import serializers
from .models import Grupo
from estudiante.serializers import EstudianteLista

from profesor.serializers import ProfesorMeSerializer
from profesor.models import Profesor

from monitor_academico.serializers import MonitorAcademicoMeSerializer
from monitor_academico.models import MonitorAcademico

class GrupoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grupo
        fields = '__all__'
        depth = 1

class GrupoListaSerializer(serializers.ModelSerializer):
    estudiantes = serializers.SerializerMethodField()
    total_estudiantes = serializers.SerializerMethodField()

    class Meta:
        model = Grupo
        fields = '__all__'
        depth = 1

    def get_estudiantes(self, obj):
        try:
            inscripciones = obj.matricula.all()
            estudiantes_data = []
            
            for inscripcion in inscripciones:
                estudiante = inscripcion.id_estudiante
                estudiante_data = {
                    'id_estudiante': estudiante.id_estudiante,
                    'nombre': estudiante.nombre,
                    'apellido': estudiante.apellido,
                    'numero_documento': estudiante.numero_documento,
                    'email': estudiante.email,
                    'colegio': estudiante.colegio,
                    'tipo_vinculacion': inscripcion.tipo_vinculacion,
                }
                estudiantes_data.append(estudiante_data)
            
            return estudiantes_data
        except Exception as e:
            print(f"Error obteniendo estudiantes: {e}")
            return []

    def get_total_estudiantes(self, obj):
        return obj.matricula.count()
