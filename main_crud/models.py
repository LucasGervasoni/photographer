from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Orders

class Orders(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  date = models.DateField()
  time = models.TimeField()
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  addressTwo = models.CharField(max_length=150, verbose_name="Address 2")
  zipCode = models.CharField(max_length=50, verbose_name="Zip Code")
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  services = models.CharField(max_length=300)

  def __str__(self):
    return "{} -> {} | {} at {}".format(self.user, self.addressOne, self.date, self.time)

  