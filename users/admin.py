from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ['username','firstName', 'lastName','phoneOne', 'phoneTwo' , 'address']
 search_fields = ['firstName', 'lastName', 'address']