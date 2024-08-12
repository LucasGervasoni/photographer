from django.contrib import admin
from .models import OrderImage, UserAction
from rangefilter.filters import (
    DateRangeFilterBuilder
)
# Register your models here.
@admin.register(OrderImage)
class OrderImageAdmin(admin.ModelAdmin):
 list_display = ['order','image', 'uploaded_at','services','scan_url','photos_sent','photos_returned']
 list_filter = (("uploaded_at", DateRangeFilterBuilder()),)
 ordering = ('-uploaded_at',)
 
 @admin.register(UserAction)
 class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'action_date', 'order', 'order_image')
    list_filter = (("action_date", DateRangeFilterBuilder()),'action_type', 'user',)
    search_fields = ('user__username', 'action_type', 'order__id', 'order_image__id')
