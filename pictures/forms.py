from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
  photo = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control align-self-center w-50 formFiles ml-auto mr-auto",
            "multiple": "True",
        }))
  class Meta:
    model = Image
    fields = '__all__'
    labels = {'photo':''}