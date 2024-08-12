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
    ("Floor Plan","Floor Plan")
  )
  
  status = (
    ("Not Uploaded","Not Uploaded"),
    ("Production","Production"),
    ("Completed","Completed"),
  )
  
  user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Photographer")
  customer = models.CharField(max_length=150, verbose_name="Customer")
  scheduled = models.DateTimeField(verbose_name="Scheduled", null=True)
  address = models.CharField(max_length=200, verbose_name="Address")
  services = MultiSelectField(choices=services_choices)
  order_status = models.CharField(choices=status, null=False, blank=False, default="Not Uploaded", verbose_name="Status")
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return "Photographer: {}, Order: {}".format(self.user, self.address)

  