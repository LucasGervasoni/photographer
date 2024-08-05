from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class File(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  photo = models.FileField(upload_to="media", verbose_name="Upload Your file")
  order = models.CharField(help_text="Enter the Address:")
  editor_notes = models.CharField(max_length=300,null=True,blank=True, verbose_name="Editor Notes")
  created_date = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return "{} -> {} | {} ".format(self.order, self.editor_notes, self.created_date)