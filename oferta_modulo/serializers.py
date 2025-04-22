from rest_framework import serializers
from .models import OfertaModulo

class OfertaModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaModulo
        fields = '__all__'
        read_only_fields = ('id_oferta_modulo',)