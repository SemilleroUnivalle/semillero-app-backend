from rest_framework import serializers
from .models import OfertaAcademica

class OfertaAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaAcademica
        fields = '__all__'
        read_only_fields = ('id_oferta_academica',)