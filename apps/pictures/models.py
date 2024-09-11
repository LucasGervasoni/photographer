from django.db import models
from apps.main_crud.models import Order
import os
from multiselectfield import MultiSelectField
from django.conf import settings
import rawpy
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
from moviepy.editor import VideoFileClip
import imageio
import tempfile
# # Create your models here.


def order_image_path(instance, filename, relative_path=None):
    if relative_path is None and hasattr(instance, 'relative_path_temp'):
        relative_path = instance.relative_path_temp
    else:
        instance.relative_path_temp = relative_path

    order_address = slugify(instance.order.address)

    existing_groups = OrderImageGroup.objects.filter(order=instance.order)
    group_count = existing_groups.count() if existing_groups.exists() else 1

    if group_count > 2:
        group_count -= 1

    base_path = os.path.join('media', order_address, f'{order_address}.{group_count:02d}')

    if relative_path:
        base_path = os.path.join(base_path, relative_path)

    # Use the original filename
    final_path = os.path.join(base_path, filename)

    # Ensure the file name is unique if a file with the same name already exists
    counter = 1
    file_root, file_extension = os.path.splitext(filename)
    while os.path.exists(final_path):
        final_path = os.path.join(base_path, f"{file_root}_{counter}{file_extension}")
        counter += 1

    return final_path


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
    created_by_view = models.CharField(max_length=100, blank=True, null=True)
    zip_file_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Group for {self.order} - Created at {self.created_at}"
    
    class Meta:
        verbose_name = "Order File Created "  # Singular name
        verbose_name_plural = "Order Files Created"  # Plural name (optional)

class OrderImage(models.Model):
    
    order = models.ForeignKey(Order, related_name='image', on_delete=models.CASCADE)
    image = models.FileField(upload_to=order_image_path, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    photos_sent = models.CharField(verbose_name="Assets to be uploaded", max_length=150)
    photos_returned = models.CharField(verbose_name="Assets to be returned", max_length=150, default="0")
    group = models.ForeignKey(OrderImageGroup, on_delete=models.CASCADE, related_name='images')
    converted_image = models.ImageField(upload_to='converted_images/', blank=True, null=True)
    selected_for_exclusion = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.order}"
    
    class Meta:
        verbose_name = "File uploaded"  # Singular name
        verbose_name_plural = "Files uploaded"  # Plural name (optional)
        
    def get_order_address_folder(self):
        """
        Get the folder path for this order based on the order's address.
        The converted image will be saved in the 'converted_image' folder inside this directory.
        """
        order_address = self.order.address  # Assuming 'address' is a field in the Order model
        return os.path.join(order_address, 'converted_image')
        
    def convert_to_jpeg(self):
        file_extension = self.image.name.split('.')[-1].lower()
        
        if file_extension in ['raw', 'dng', 'arw']:
            # Process RAW files using rawpy
            with rawpy.imread(self.image) as raw:
                rgb = raw.postprocess()

            image = Image.fromarray(rgb)
            image_io = ContentFile(b'')
            image.save(image_io, format='PNG')

        elif file_extension in ['hevc', 'heic']:
            # Process HEVC/HEIC files using imageio
            with self.image.open('rb') as file:
                image = imageio.imread(file, format='heic')

            image = Image.fromarray(image)
            image_io = ContentFile(b'')
            image.save(image_io, format='PNG')

        else:
            # If not a supported format, return None
            return None

        image_name_without_extension = os.path.splitext(os.path.basename(self.image.name))[0]
        converted_image_path = os.path.join('converted_images',self.get_order_address_folder(), f'{image_name_without_extension}.png')
        
        # Save the converted image using default_storage (Django default)
        self.converted_image.name = default_storage.save(converted_image_path, image_io)
        self.save()  # Save the model instance with the converted image

        # Return the URL directly
        return default_storage.url(self.converted_image.name)
    
    def convert_video_to_thumbnail(self):
        video_extensions = ['mp4', 'mov', 'avi', 'mkv']
        file_extension = self.image.name.split('.')[-1].lower()

        if file_extension in video_extensions:
            # Open the file directly from the backend storage
            with self.image.open('rb') as video_file:
                # Create a temporary file to store the video
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_video:
                    temp_video.write(video_file.read())
                    temp_video_path = temp_video.name

            # Now use temporary file path with VideoFileClip
            try:
                video = VideoFileClip(temp_video_path)

               # Extract the first frame
                thumbnail_frame = video.get_frame(0)
                image = Image.fromarray(thumbnail_frame)

                image_io = ContentFile(b'')
                image.save(image_io, format='PNG')

                image_name_without_extension = os.path.splitext(os.path.basename(self.image.name))[0]
                thumbnail_path = os.path.join('converted_images',self.get_order_address_folder(), f'{image_name_without_extension}.png')

                self.converted_image.name = default_storage.save(thumbnail_path, image_io)
                self.save()
            finally:
                # Make sure to close VideoFileClip and remove the temporary file
                video.close()
                os.remove(temp_video_path)

            return self.converted_image.url
        return None
    
    def convert_media(self):
        """
        This method will try to convert the file either using convert_to_jpeg or convert_video_to_thumbnail
        depending on the file type.
        """
        # Try to convert raw image files first
        if not self.convert_to_jpeg():
            # If not a raw image, try to convert video files
            self.convert_video_to_thumbnail()

        
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