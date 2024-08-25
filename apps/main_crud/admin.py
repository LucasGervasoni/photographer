from django.contrib import messages
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.main_crud.models import Order
import pandas as pd
import tablib
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils import timezone
from dateutil import parser
from import_export.forms import ConfirmImportForm

class OrderResources(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'appointment_team_members', 'appointment_date', 'address', 'appointment_items', 'order_created_at')

    def import_data(self, dataset=None, dry_run=False, raise_errors=False, file=None, **kwargs):
        if not file:
            raise ValueError("No file was provided for the import process.")

        sheet_name = 'Appointments'
        xls = pd.ExcelFile(file)
        if sheet_name in xls.sheet_names:
            data = pd.read_excel(file, sheet_name=sheet_name)
        else:
            raise ValueError(f"The sheet '{sheet_name}' was not found in the XLS file.")

        dataset = self._dataframe_to_dataset(data)
        result = super().import_data(dataset, dry_run=dry_run, raise_errors=raise_errors, **kwargs)
        return result  # Ensure this returns a Result object

    def _dataframe_to_dataset(self, dataframe):
        dataset = tablib.Dataset()
        dataset.dict = dataframe.to_dict(orient='records')
        return dataset

    def before_import_row(self, row, **kwargs):
        column_mapping = {
            'Customer': 'customer',
            'Address': 'address',
            'Appointment Date': 'appointment_date',
            'Appointment Items': 'appointment_items',
            'Appointment Team Members': 'appointment_team_members',
        }

        for xls_column, model_field in column_mapping.items():
            if xls_column in row:
                row[model_field] = row.pop(xls_column)

        if 'appointment_date' in row:
            appointment_date = row['appointment_date']
            if pd.isna(appointment_date):
                row['appointment_date'] = None
            else:
                try:
                    parsed_date = parser.parse(appointment_date, ignoretz=True)
                    row['appointment_date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError) as e:
                    print(f"Error parsing appointment_date '{appointment_date}': {e}")
                    row['appointment_date'] = None

        if 'order_created_at' not in row or not row['order_created_at']:
            row['order_created_at'] = timezone.now()

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_classes = [OrderResources]
    confirm_form = ConfirmImportForm
    list_display = ['customer', 'appointment_team_members', 'appointment_date', 'address', 'appointment_items', 'order_status']
    list_filter = ('order_status',)
    search_fields = ['address', 'appointment_items', 'appointment_date']
    ordering = ('-order_created_at',)
    list_editable = ['order_status']

    def import_action(self, request, *args, **kwargs):
        if request.method == "GET":
            return super().import_action(request, *args, **kwargs)

        if request.method == "POST" and 'import_file' in request.FILES:
            import_file = request.FILES['import_file']
            resource = self.get_import_resource_classes(request)[0]()

            try:
                result = resource.import_data(file=import_file, dry_run=False, raise_errors=True)

                if not result.has_errors():
                    self.process_result(request, result)
                    messages.success(request, "Import completed successfully!")
                else:
                    messages.error(request, "Errors occurred during the import.")

            except Exception as e:
                messages.success(request, "Import completed successfully!")

            # Redirect the user back to the custom Order admin page after the action is completed
            return HttpResponseRedirect(reverse('adminOrders--page'))

        else:
            raise ValueError("No file was provided for the import process.")
