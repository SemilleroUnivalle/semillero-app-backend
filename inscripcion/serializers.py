from rest_framework import serializers
from .models import Inscripcion

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'
        read_only_fields = ('id_inscripcion',)