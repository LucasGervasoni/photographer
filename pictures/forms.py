from django import forms
from .models import OrderImage

class OrderImageForm(forms.ModelForm):
  class Meta:
    model = OrderImage
    fields = ['image', 'editor_note']
    widgets = {
            'editor_note': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }


class PhotographerImageForm(forms.ModelForm):
    class Meta:
        model = OrderImage
        fields = ['image']  # Only image field
