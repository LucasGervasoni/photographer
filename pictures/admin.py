from django.contrib import admin
from .models import OrderImage
from rangefilter.filters import (
    DateRangeFilterBuilder
)
# Register your models here.
@admin.register(OrderImage)
class OrderImageAdmin(admin.ModelAdmin):
 list_display = ['order','image', 'uploaded_at']
 list_filter = (("uploaded_at", DateRangeFilterBuilder()),)
 ordering = ('-uploaded_at',)
