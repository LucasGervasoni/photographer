from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
# Create your models here.

#Orders

class Order(models.Model):
  
  services_choices = (
    ("Drone","Drone"),
    ("Photo","Photo"),
    ("3d scan","3d scan"),
    ("Vídeo","Vídeo"),
  )
  
  status = (
    ("Not Uploaded","Not Uploaded"),
    ("Production","Production"),
    ("Completed","Completed"),
  )
  
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  date = models.DateField()
  time = models.TimeField()
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  addressTwo = models.CharField(max_length=150, verbose_name="Address 2", null=True, blank=True)
  zipCode = models.CharField(max_length=50, verbose_name="Zip Code", null=True, blank=True)
  city = models.CharField(max_length=50, help_text='Ex: San Francisco')
  state = models.CharField(max_length=50, help_text='Ex: CA')
  services = MultiSelectField(choices=services_choices)
  order_status = models.CharField(choices=status, null=False, blank=False, default="Not Uploaded", verbose_name="Status")

  def __str__(self):
    return "{} -> {} | {} at {}".format(self.user, self.addressOne, self.date, self.time)

  