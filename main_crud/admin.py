from django.contrib import admin
from .models import Order

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils import timezone
from dateutil import parser
# Register your models here.

class OrderResoucers(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id','customer','appointment_team_members','appointment_date', 'address', 'appointment_items','order_created_at')
        
    def before_import_row(self, row, **kwargs):
        
        # Mapping XLS columns to column names in the database
        column_mapping = {
            'Customer': 'customer',
            'Address': 'address',
            'Appointment Date': 'appointment_date',
            'Appointment Items': 'appointment_items',
            'Appointment Team Members': 'appointment_team_members',
        }
        
        # Rename the columns according to the mapping
        for xls_column, model_field in column_mapping.items():
            if xls_column in row:
                row[model_field] = row.pop(xls_column)
        
        
          # Processamento da coluna 'appointment_date'
        if 'appointment_date' in row:
            appointment_date = row['appointment_date']
            if appointment_date:  # Verifica se a data não é None ou vazia
                try:
                    # Tenta fazer o parsing da data usando o dateutil.parser
                    parsed_date = parser.parse(appointment_date, ignoretz=True)
                    # Formata a data no formato desejado "2024-08-07 08:00:00"
                    row['appointment_date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError) as e:
                    print(f"Error parsing appointment_date '{appointment_date}': {e}")
                    row['appointment_date'] = None  # Ou você pode escolher manter o valor original, dependendo do caso de uso
            else:
                print("Appointment date is empty or None.")
                row['appointment_date'] = None  # Definir como None se a data for vazia
        else:
            print("Appointment date column not found.")
            row['appointment_date'] = None  # Definir como None se a chave não existir

       # Check and set order_created_at if not defined
        if 'order_created_at' not in row or not row['order_created_at']:
            row['order_created_at'] = timezone.now()

@admin.register(Order)
class ProfileAdmin(ImportExportModelAdmin):
 resource_classes = [OrderResoucers]
 list_display = ['customer','appointment_team_members','appointment_date','address','appointment_items', 'order_status']
 list_filter = ('order_status',)
 search_fields = ['address', 'appointment_items','appointment_date',]
 ordering = ('-order_created_at',)
 list_editable = ['order_status']
 
 def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.GET.get('appointment_team_members') and request.GET.get('address'):
            form.base_fields['appointment_team_members'].initial = request.GET['appointment_team_members']
            form.base_fields['address'].initial = request.GET['address']
        return form