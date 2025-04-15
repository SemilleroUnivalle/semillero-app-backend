from rest_framework import serializers
from .models import GradoEscolar

class GradoEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradoEscolar
        fields = '__all__'
