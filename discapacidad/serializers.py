from rest_framework import serializers
from .models import Discapacidad

class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'nombre': {'required': True},
            'descripcion': {'required': True},
        }