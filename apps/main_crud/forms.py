from django import forms
from apps.main_crud.models import Order
from apps.pictures.models import OrderImageGroup

class OrderForm(forms.ModelForm):
    
    appointment_items = forms.MultipleChoiceField(
        choices=OrderImageGroup.select_services,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Services"
    )
     
    class Meta:
        model = Order
        fields = ['appointment_team_members', 'customer', 'appointment_date', 'address', 'appointment_items', 'order_status']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'order_status': forms.Select(),
        }
