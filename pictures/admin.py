from django.contrib import admin
from .models import OrderImage, UserAction, OrderImageGroup
from rangefilter.filters import (
    DateRangeFilterBuilder
)
# Register your models here.
@admin.register(OrderImage)
class OrderImageAdmin(admin.ModelAdmin):
 list_display = ['order','image', 'uploaded_at','photos_sent','photos_returned']
 list_filter = (("uploaded_at", DateRangeFilterBuilder()),)
 ordering = ('-uploaded_at',)
 
 @admin.register(UserAction)
 class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'action_date', 'order', 'order_image')
    list_filter = (("action_date", DateRangeFilterBuilder()),'action_type', 'user',)
    search_fields = ('user__username', 'action_type', 'order__id', 'order_image__id')


@admin.register(OrderImageGroup)
class GroupFiles(admin.ModelAdmin):
    list_display = ('order','editor_note','services','scan_url', 'created_at')
    list_filter = (("created_at", DateRangeFilterBuilder()),)