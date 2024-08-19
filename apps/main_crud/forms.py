from django import forms
from apps.main_crud.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['appointment_team_members', 'customer', 'appointment_date', 'address', 'appointment_items', 'order_status']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'order_status': forms.Select(),
        }
