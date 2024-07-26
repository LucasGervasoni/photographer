from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  username = models.OneToOneField(User, on_delete=models.CASCADE)
  firstName = models.CharField(max_length=150)
  lastName = models.CharField(max_length=150)
  phoneOne = models.CharField(max_length=100)
  phoneTwo = models.CharField(max_length=100)
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  addressTwo = models.CharField(max_length=150, verbose_name="Address 2")
  zipCode = models.CharField(max_length=50, verbose_name="Zip Code")
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)

  def __str__(self):
    return "{}".format(self.username)