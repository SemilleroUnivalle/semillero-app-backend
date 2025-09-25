from rest_framework import serializers
from .models import MonitorAdministrativo

class MonitorAdministrativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorAdministrativo
        fields = '__all__' 