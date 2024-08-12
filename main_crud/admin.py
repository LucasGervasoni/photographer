from django.contrib import admin
from .models import Order

from rangefilter.filters import (
    DateRangeFilterBuilder
)

# Register your models here.
@admin.register(Order)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ['user','scheduled','address','services', 'order_status', 'date']
 list_filter = (("date", DateRangeFilterBuilder()), 'order_status')
 search_fields = ['address', 'services']
 ordering = ('-date',)
 list_editable = ['order_status']
