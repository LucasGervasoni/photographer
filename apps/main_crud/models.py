from django.conf import settings
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
  
  # Override the save method to ensure order_created_at is not null
  def save(self, *args, **kwargs):
        if not self.order_created_at:
            self.order_created_at = timezone.now()
        super().save(*args, **kwargs)

class OrderEditorAssignment(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    assigned_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.id} - Editor: {self.assigned_editor.get_full_name() if self.assigned_editor else 'None'}"