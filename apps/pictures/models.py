from io import BytesIO
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
import pillow_heif
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
    all_converted = models.BooleanField(default=False)
    
    def check_all_converted(self):
        """
        Verifica se todas as imagens associadas ao grupo foram convertidas.
        """
        all_converted = all(image.converted_image for image in self.images.all())
        self.all_converted = all_converted
        self.save()
        return all_converted

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
    converted_image = models.ImageField(upload_to='converted_images/', blank=True, null=True, max_length=500)
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
    
    def compress_webp(self, image, max_size_mb=1, quality=85):
        """
        Compress the image to WebP format and ensure it does not exceed max_size_mb.
        The image will be resized if necessary. The quality parameter adjusts the compression level.
        """
        
        image_io = ContentFile(b'')
        image.save(image_io, format='WEBP', quality=quality, optimize=True)

        # Check the size of the image in MB
        size_in_mb = image_io.tell() / (512 * 512)
        
        if size_in_mb > max_size_mb:
            # If the file is larger than max_size_mb, resize it
            width, height = image.size
            resize_factor = (max_size_mb / size_in_mb) ** 0.5  # Reduce both width and height proportionally
            new_width = int(width * resize_factor)
            new_height = int(height * resize_factor)
            
            # Resize the image using LANCZOS resampling
            image = image.resize((new_width, new_height), Image.LANCZOS)

            # Save the resized image as WebP with reduced quality
            image_io = ContentFile(b'')
            image.save(image_io, format='WEBP', quality=quality, optimize=True)

        return image_io

    
    def save_compressed_image(self, image, file_basename, quality=85):
        """
        Save the compressed WebP image using Django's default storage and return the URL.
        Verifies if the file already exists before saving.
        """
        converted_image_path = os.path.join('converted_images', self.get_order_address_folder(), f'{file_basename}.webp')

        # Se o arquivo não existir, faz a compressão e salva
        compressed_image = self.compress_webp(image, max_size_mb=1, quality=quality)
        
        self.converted_image.name = default_storage.save(converted_image_path, compressed_image)
        self.save()

        return default_storage.url(self.converted_image.name)
    
    def compress_and_convert(self):
        """
        Converte uma cópia da imagem carregada para WebP, comprimida para um tamanho menor que 1MB, sem modificar a imagem original.
        """
        try:
            # Mantém o arquivo original sem modificações
            original_file_extension = self.image.name.split('.')[-1].lower()

            # Processa a imagem original e prepara a conversão
            if original_file_extension in ['heic', 'heif', 'hevc']:
                with self.image.open('rb') as image_file:
                    heif_image = pillow_heif.read_heif(image_file.read())
                    image = Image.frombytes(
                        heif_image.mode,
                        heif_image.size,
                        heif_image.data,
                        "raw",
                        heif_image.mode,
                        heif_image.stride,
                    ).convert('RGB')  # Converte para RGB
            elif original_file_extension in ['raw', 'dng', 'arw']:
                with rawpy.imread(self.image) as raw:
                    rgb = raw.postprocess()

                image = Image.fromarray(rgb).convert('RGB')  # Converte para RGB
            else:
                # Abre o arquivo e converte para RGB (não altera o arquivo original)
                image = Image.open(self.image).convert('RGB')

            # Cria um buffer para salvar a imagem convertida como WebP
            quality = 50  # Inicia com uma qualidade de 85
            while True:
                image_io = BytesIO()
                image.save(image_io, format='WEBP', quality=quality)

                # Verifica o tamanho do arquivo WebP
                webp_size = image_io.tell()

                # Se o arquivo for menor que 1MB, sai do loop
                if webp_size <= 1 * 512 * 512 or quality <= 10:
                    break

                # Reduz a qualidade se o arquivo for maior que 1MB
                quality -= 5

            # Gera o caminho correto para salvar o arquivo WebP convertido
            file_basename = os.path.splitext(os.path.basename(self.image.name))[0]
            order_folder = self.get_order_address_folder()  # Retorna o caminho correto
            converted_image_path = os.path.join('converted_images', order_folder, f'{file_basename}.webp')

            # Salva a imagem convertida no campo `converted_image` (não afeta o campo `image`)
            self.converted_image.save(converted_image_path, ContentFile(image_io.getvalue()), save=False)
            self.save()

            # Retorna a URL da imagem convertida, agora salva como WebP
            return default_storage.url(self.converted_image.name)

        except Exception as e:
            print(f"Error converting image to WebP: {e}")
            return None

    def convert_video_to_thumbnail(self):
        """
        Convert the first frame of a video to a WebP thumbnail.
        """
        video_extensions = ['mp4', 'mov', 'avi', 'mkv']
        file_extension = self.image.name.split('.')[-1].lower()

        if file_extension in video_extensions:
            # Open the file directly from the backend storage
            with self.image.open('rb') as video_file:
                # Create a temporary file to store the video
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_video:
                    temp_video.write(video_file.read())
                    temp_video_path = temp_video.name

            try:
                # Use temporary file path with VideoFileClip
                video = VideoFileClip(temp_video_path)

                # Extract the first frame
                thumbnail_frame = video.get_frame(0)
                image = Image.fromarray(thumbnail_frame)

                # Save the compressed thumbnail and return the URL
                image_name_without_extension = os.path.splitext(os.path.basename(self.image.name))[0]
                return self.save_compressed_image(image, image_name_without_extension)
                    
            finally:
                # Make sure to close VideoFileClip and remove the temporary file
                video.close()
                os.remove(temp_video_path)
        
        return None

    def convert_media(self):
        """
        This method will try to convert the file either using compress_and_convert or convert_video_to_thumbnail
        depending on the file type.
        """
        # Try to convert raw image files first
        if not self.compress_and_convert():
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