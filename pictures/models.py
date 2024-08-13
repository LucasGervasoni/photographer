from django.db import models
from main_crud.models import Order
from django.contrib.auth.models import User
import os
from django.utils.text import slugify

from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField

# # Create your models here.

# create a path and rename the images
def order_image_path(instance, filename):
    # Define your custom folder structure and file name
    order_address = instance.order.address
    order_service = instance.order.appointment_items
    order_name = "Spotlight" 
    ext = filename.split('.')[-1]
    
    # Count the number of images already uploaded for this order
    count = OrderImage.objects.filter(order=instance.order).count() + 1
    
    new_filename = f"{order_name}.{count:02d}.{ext}"
    return os.path.join('media', str(order_address), str(order_service), new_filename)

# Model base for image
class OrderImage(models.Model):
    
    select_services = (
        ("Drone","Drone"),
        ("Photo","Photo"),
        ("3d scan","3d scan"),
        ("Vídeo","Vídeo"),
        ("Floor Plan","Floor Plan")
    )
    
    
    order = models.ForeignKey(Order, related_name='image', on_delete=models.CASCADE)
    image = models.FileField(upload_to=order_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    editor_note = models.TextField(blank=True, null=True) 
    services = MultiSelectField(choices=select_services, blank=True)
    scan_url = models.CharField(max_length=200, blank=True, null=True)
    photos_sent = models.CharField(verbose_name="Assets to be uploaded")
    photos_returned = models.CharField(verbose_name="Assets to be uploaded")
    
    def __str__(self):
        return f"Image for {self.order} - Service: {self.services}"
    
    class Meta:
        verbose_name = "Order File"  # Singular name
        verbose_name_plural = "Order Files"  # Plural name (optional)

# Upload automatic for order status    
@receiver(post_save, sender=OrderImage)
def update_order_status(sender, instance, **kwargs):
    order = instance.order
    if order.order_status == "Not Uploaded":
        order.order_status = "Production"
        order.save()
        
# Create User actions that will take automatic the user that did Upload or Download
class UserAction(models.Model):
    ACTION_CHOICES = [
        ('download', 'Download'),
        ('upload', 'Upload'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)
    order_image = models.ForeignKey(OrderImage, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.action_date}"