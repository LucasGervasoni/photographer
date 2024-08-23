from django.db import models
from apps.main_crud.models import Order
import os
from multiselectfield import MultiSelectField
from django.conf import settings
import rawpy
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# # Create your models here.

# Function to generate the upload path
def order_image_path(instance, filename):
    order_address = instance.order.address.replace(' ', '_')
    group_count = OrderImageGroup.objects.filter(order=instance.order).count()

    # Extract the file extension
    extension = filename.split('.')[-1]
    # Generate a base filename
    base_filename = f'Spotlight{instance.group.images.count() + 1:02d}.{extension}'
    
    # Define the initial path
    path = os.path.join('media', order_address, f'{order_address}.{group_count:02d}', base_filename)
    
    # Check if the file already exists and append a suffix if necessary
    counter = 1
    while os.path.exists(path):
        base_filename = f'Spotlight{instance.group.images.count() + 1:02d}_{counter}.{extension}'
        path = os.path.join('media', order_address, f'{order_address}.{group_count:02d}', base_filename)
        counter += 1

    return path


# Model base for image
class OrderImageGroup(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    editor_note = models.TextField(blank=True, null=True)
    
    select_services = (
        ("Drone Vídeo", "Drone Vídeo"),
        ("Drone Photo", "Drone Photo"),
        ("Photo", "Photo"),
        ("3d scan", "3d scan"),
        ("Video", "Video"),
        ("Floor Plan", "Floor Plan"),
    )
    
    services = MultiSelectField(choices=select_services, blank=True)
    scan_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Group for {self.order} - Created at {self.created_at}"
    
    class Meta:
        verbose_name = "Order File Created "  # Singular name
        verbose_name_plural = "Order Files Created"  # Plural name (optional)

class OrderImage(models.Model):
    
    order = models.ForeignKey(Order, related_name='image', on_delete=models.CASCADE)
    image = models.FileField(upload_to=order_image_path, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    photos_sent = models.CharField(verbose_name="Assets to be uploaded")
    photos_returned = models.CharField(verbose_name="Assets to be returned", required=False)
    group = models.ForeignKey(OrderImageGroup, on_delete=models.CASCADE, related_name='images')
    converted_image = models.ImageField(upload_to='converted_images/', blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.order}"
    
    class Meta:
        verbose_name = "File uploaded"  # Singular name
        verbose_name_plural = "Files uploaded"  # Plural name (optional)
        

    def convert_to_jpeg(self):
        file_extension = self.image.name.split('.')[-1].lower()
        if file_extension in ['raw', 'dng', 'arw']:
            with rawpy.imread(self.image) as raw:
                rgb = raw.postprocess()

            image = Image.fromarray(rgb)
            image_io = ContentFile(b'')
            image.save(image_io, format='JPEG')

            image_name_without_extension = os.path.splitext(os.path.basename(self.image.name))[0]

            # Definir o caminho de salvamento em media/converted_images/
            converted_image_path = os.path.join('converted_images', f'{image_name_without_extension}.jpeg')
            
            # Salvar a imagem convertida usando o default_storage (padrão do Django)
            self.converted_image.name = default_storage.save(converted_image_path, image_io)
            self.save()  # Salvar a instância do modelo com a imagem convertida

            # Retornar a URL diretamente
            return default_storage.url(self.converted_image.name)
        return None

        
# Create User actions that will take automatic the user that did Upload or Download
class UserAction(models.Model):
    ACTION_CHOICES = [
        ('download', 'Download'),
        ('upload', 'Upload'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)
    order_image = models.ForeignKey(OrderImage, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.action_date}"