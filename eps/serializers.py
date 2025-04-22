from rest_framework import serializers
from .models import EPS

class EPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPS
        fields = '__all__'
        read_only_fields = ('id_eps',)