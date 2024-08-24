from django import forms
from apps.pictures.models import OrderImage, OrderImageGroup

class OrderImageForm(forms.ModelForm):
    class Meta:
        model = OrderImage
        fields = ['image','photos_sent', 'photos_returned']
        widgets = {
            'photos_sent': forms.NumberInput(attrs={'min': 0}),
            'photos_returned': forms.NumberInput(attrs={'min': 0}),
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderImageForm, self).__init__(*args, **kwargs)
        self.fields['photos_returned'].required = False

class PhotographerImageForm(forms.ModelForm):
    class Meta:
        model = OrderImage
        fields = ['image']

# Optional: A new form to handle editor notes for OrderImageGroup
class OrderImageGroupForm(forms.ModelForm):
    class Meta:
        model = OrderImageGroup
        fields = ['services', 'scan_url', 'editor_note']
        widgets = {
            'editor_note': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'scan_url': forms.URLInput(attrs={'placeholder': 'Enter URL for 3d scan'}),
            'services': forms.CheckboxSelectMultiple,
        }
