from rest_framework import serializers
from .models import HistorialCambios

class HistorialCambiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialCambios
        fields = '__all__'
        read_only_fields = ('id_historial',)