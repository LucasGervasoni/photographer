from django.contrib import admin
from .models import Order

# Register your models here.

@admin.register(Order)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ['user','scheduled', 'time','addressOne', 'addressTwo','zipCode','city', 'state','services', 'order_status', 'date']
 list_filter = [ 'order_status','state', 'date']
 search_fields = ['addressOne', 'addressTwo','zipCode','city', 'state', 'services']
