from django import forms
from .models import OrderImage

class OrderImageForm(forms.ModelForm):
  class Meta:
    model = OrderImage
    fields = ['image'] 
