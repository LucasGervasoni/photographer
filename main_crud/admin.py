from django.contrib import admin
from .models import Order

from rangefilter.filters import (
    DateRangeFilterBuilder
)

from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

class OrderResoucers(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id','customer','appointment_team_members','appointment_date', 'address', 'appointment_items','order_created_at')
    

@admin.register(Order)
class ProfileAdmin(ImportExportModelAdmin):
 resource_classes = [OrderResoucers]
 list_display = ['customer','appointment_team_members','appointment_date','address','appointment_items', 'order_status', 'order_created_at']
 list_filter = (("order_created_at", DateRangeFilterBuilder()), 'order_status')
 search_fields = ['address', 'appointment_items']
 ordering = ('-order_created_at',)
 list_editable = ['order_status']