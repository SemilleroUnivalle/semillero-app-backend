from rest_framework import serializers
from .models import Modulo

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'
        read_only_fields = ('id_modulo',)