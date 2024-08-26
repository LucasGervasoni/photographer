from django import forms
from apps.main_crud.models import Order
from apps.pictures.models import OrderImageGroup
from apps.users.models import CustomUser

class OrderForm(forms.ModelForm):
    
    appointment_team_members = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select,
        required=True,
        label="Appointment Member"
    )
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['appointment_team_members'].label_from_instance = lambda obj: f"{obj.get_full_name()}"
    
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
