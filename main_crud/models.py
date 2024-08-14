from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
# Create your models here.

#Orders

class Order(models.Model):
  
  status = (
    ("Not Uploaded","Not Uploaded"),
    ("Production","Production"),
    ("Completed","Completed"),
  )
  
  appointment_team_members = models.CharField(max_length=300,verbose_name="Appointment Member")
  customer = models.CharField(max_length=200, verbose_name="Customer")
  appointment_date = models.CharField(verbose_name="Scheduled", null=True)
  address = models.CharField(max_length=200, verbose_name="Address")
  appointment_items = models.CharField(max_length=200, verbose_name="Services")
  order_status = models.CharField(choices=status, null=False, blank=False, default="Not Uploaded", verbose_name="Status")
  order_created_at = models.CharField(editable=False, verbose_name="Created At")

  def __str__(self):
    return "Photographer: {}, Order: {}".format(self.appointment_team_members, self.address)

  