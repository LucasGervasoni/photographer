from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Orders

class Orders(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  date = models.DateField(help_text='MM/DD/YY')
  time = models.TimeField(help_text='Ex: 3:00 to AM or 15:00 to PM')
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  addressTwo = models.CharField(max_length=150, verbose_name="Address 2", null=True, blank=True)
  zipCode = models.CharField(max_length=50, verbose_name="Zip Code", null=True, blank=True)
  city = models.CharField(max_length=50, help_text='Ex: San Francisco')
  state = models.CharField(max_length=50, help_text='Ex: CA')
  services = models.CharField(max_length=300, help_text='Ex: Drone; Vídeos; Photos;')

  def __str__(self):
    return "{} -> {} | {} at {}".format(self.user, self.addressOne, self.date, self.time)

  