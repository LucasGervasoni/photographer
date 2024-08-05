from django.contrib import admin
from .models import File

from rangefilter.filters import (
    DateRangeFilterBuilder
)
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
 list_display = ['id', 'author', 'order', 'photo', 'editor_notes', 'created_date']
 list_filter = (("created_date", DateRangeFilterBuilder()), 'author')
 search_fields = ['author', 'order','created_date','id']
 ordering = ('-created_date',)