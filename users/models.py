from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Artists Profile
class Profile(models.Model):
  username = models.OneToOneField(User, on_delete=models.CASCADE)
  firstName = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  phoneOne = models.CharField(max_length=100, verbose_name="Phone 1")
  phoneTwo = models.CharField(max_length=100, verbose_name="Phone 2", null=True, blank=True)
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  addressTwo = models.CharField(max_length=150, verbose_name="Address 2", null=True, blank=True)
  zipCode = models.CharField(max_length=50, verbose_name="Zip Code", null=True, blank=True)
  city = models.CharField(max_length=50, help_text='Ex: San Francisco')
  state = models.CharField(max_length=50, help_text='Ex: CA')

  def __str__(self):
    return "{}".format(self.username)