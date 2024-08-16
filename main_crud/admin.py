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
 list_filter = ('order_status',)
 search_fields = ['address', 'appointment_items', 'order_created_at','appointment_date',]
 ordering = ('-id',)
 list_editable = ['order_status']
 
 def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.GET.get('appointment_team_members') and request.GET.get('address'):
            form.base_fields['appointment_team_members'].initial = request.GET['appointment_team_members']
            form.base_fields['address'].initial = request.GET['address']
        return form