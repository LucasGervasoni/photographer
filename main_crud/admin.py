from django.contrib import admin
from .models import Order

from rangefilter.filters import (
    DateRangeFilterBuilder
)

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils import timezone
import re
from datetime import datetime
# Register your models here.

class OrderResoucers(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id','customer','appointment_team_members','appointment_date', 'address', 'appointment_items','order_created_at')
        
    def before_import_row(self, row, **kwargs):
         # Limpeza e formatação da data antes de salvar a instância
        if 'appointment_date' in row:
            # Procurar pela data e hora no formato "Aug 07 2024, 8:00am"
            date_match = re.search(r'\w{3} \d{2} \d{4}, \d{1,2}:\d{2}[ap]m', row['appointment_date'])
            if date_match:
                # Converter a string encontrada para um objeto datetime
                parsed_date = datetime.strptime(date_match.group(0), '%b %d %Y, %I:%M%p')
                # Formatar a data no formato desejado (exemplo: "2024-08-07 08:00:00")
                row['appointment_date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')

        # Verifica e define order_created_at se não estiver definido
        if 'order_created_at' not in row or not row['order_created_at']:
            row['order_created_at'] = timezone.now()

@admin.register(Order)
class ProfileAdmin(ImportExportModelAdmin):
 resource_classes = [OrderResoucers]
 list_display = ['customer','appointment_team_members','appointment_date','address','appointment_items', 'order_status']
 list_filter = ('order_status',)
 search_fields = ['address', 'appointment_items','appointment_date',]
 ordering = ('order_created_at',)
 list_editable = ['order_status']
 
 def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.GET.get('appointment_team_members') and request.GET.get('address'):
            form.base_fields['appointment_team_members'].initial = request.GET['appointment_team_members']
            form.base_fields['address'].initial = request.GET['address']
        return form