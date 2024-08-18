from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)