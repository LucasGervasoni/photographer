from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Artists Profile
class Profile(models.Model):
  username = models.OneToOneField(User, on_delete=models.CASCADE)
  firstName = models.CharField(max_length=100, null=True, verbose_name="First Name")
  lastName = models.CharField(max_length=100, null=True, verbose_name="Last Name")
  phoneOne = models.CharField(max_length=100, verbose_name="Phone 1")
  phoneTwo = models.CharField(max_length=100, verbose_name="Phone 2", null=True, blank=True)
  address = models.CharField(max_length=300, verbose_name="Address")

  def __str__(self):
    return "{}".format(self.username)