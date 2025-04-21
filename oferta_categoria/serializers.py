from rest_framework import serializers
from .models import OfertaCategoria

class OfertaCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaCategoria
        fields = '__all__'
        read_only_fields = ('id_oferta_categoria',)