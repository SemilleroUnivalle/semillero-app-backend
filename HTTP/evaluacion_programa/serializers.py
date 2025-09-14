from rest_framework import serializers
from .models import EvaluacionPrograma

class EvaluacionProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionPrograma
        fields = '__all__'
        