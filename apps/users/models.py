from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"