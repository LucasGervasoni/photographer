from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
  photo = models.FileField(upload_to="media")
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  order = models.CharField(verbose_name="In which order will the upload be done?", help_text="Enter the Address:")
  editor_notes = models.CharField(max_length=300,null=True,blank=True, verbose_name="Editor Notes")
  created_date = models.DateTimeField(auto_now_add=True)