from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = '__all__'
    widgets = {
      'date' : forms.DateInput(attrs={'type' : 'date'}),
      'time' : forms.TimeInput(attrs={'type' : 'time'}),
      'services': forms.Select(attrs={"class":"form-select"}),
      'order_status': forms.Select(attrs={"class":"form-select"})
    }