from django.contrib import admin
from .models import Order

from rangefilter.filters import (
    DateRangeFilterBuilder
)

# Register your models here.

@admin.register(Order)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ['user','scheduled', 'time','addressOne', 'addressTwo','zipCode','city', 'state','services', 'order_status', 'date']
 list_filter = (("date", DateRangeFilterBuilder()), 'order_status','state')
 search_fields = ['addressOne', 'addressTwo','zipCode','city', 'state', 'services']
 ordering = ('-date',)
