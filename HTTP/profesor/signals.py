from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Profesor
from rest_framework.authtoken.models import Token
