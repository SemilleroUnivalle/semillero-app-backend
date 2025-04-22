from rest_framework import serializers
from .models import Acudiente

class AcudienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acudiente
        fields = '__all__'