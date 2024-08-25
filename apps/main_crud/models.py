from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils import timezone
# Create your models here.

#Orders

class Order(models.Model):
  
  status = (
    ("Not Uploaded","Not Uploaded"),
    ("Production","Production"),
    ("Completed","Completed"),
  )
  
  appointment_team_members = models.CharField(max_length=300,verbose_name="Appointment Member")
  customer = models.CharField(max_length=200, verbose_name="Customer", null=True,blank=True)
  appointment_date = models.DateTimeField(max_length=200,verbose_name="Scheduled", null=True)
  address = models.CharField(max_length=200, verbose_name="Address")
  appointment_items = models.CharField(max_length=200, verbose_name="Services")
  order_status = models.CharField(max_length=150,choices=status, null=False, blank=False, default="Not Uploaded", verbose_name="Status")
  order_created_at = models.DateTimeField(auto_created=True,editable=False, verbose_name="Created At")

  def __str__(self):
    return "Photographer: {}, Order: {}".format(self.appointment_team_members, self.address)
  
  # Sobrescreve o método save para garantir que order_created_at não seja nulo
  def save(self, *args, **kwargs):
        if not self.order_created_at:
            self.order_created_at = timezone.now()
        super().save(*args, **kwargs)

  