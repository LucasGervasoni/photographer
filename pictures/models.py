from django.db import models
from main_crud.models import Order

# # Create your models here.
class OrderImage(models.Model):
    order = models.ForeignKey(Order, related_name='image', on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.order}"