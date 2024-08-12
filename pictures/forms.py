from django import forms
from .models import OrderImage

class OrderImageForm(forms.ModelForm):
  class Meta:
    model = OrderImage
    fields = ['image', 'editor_note','services']
    widgets = {
            'editor_note': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'scan_url': forms.URLInput(attrs={'placeholder': 'Enter URL for 3d scan'}),
            'photos_sent': forms.NumberInput(attrs={'min': 0}),
            'photos_returned': forms.NumberInput(attrs={'min': 0}),
            'services': forms.CheckboxSelectMultiple,
        }


class PhotographerImageForm(forms.ModelForm):
    class Meta:
        model = OrderImage
        fields = ['image']  # Only image field
