from django.db import models
from main_crud.models import Order
import os
from django.utils.text import slugify
# # Create your models here.

def order_image_path(instance, filename):
    # Define your custom folder structure and file name
    order_id = instance.order.id
    order_name = slugify(instance.order)  # Assuming 'Order' has a 'name' field
    ext = filename.split('.')[-1]
    new_filename = f"{order_name}_{order_id}.{ext}"
    return os.path.join('orders', str(order_id), new_filename)


class OrderImage(models.Model):
    order = models.ForeignKey(Order, related_name='image', on_delete=models.CASCADE)
    image = models.FileField(upload_to=order_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.order}"