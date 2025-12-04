from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MonitorAdministrativo
from rest_framework.authtoken.models import Token
import threading
