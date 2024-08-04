from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ['username','firstName', 'lastName','phoneOne', 'phoneTwo' , 'addressOne', 'addressTwo', 
                 'zipCode','city', 'state']
 list_filter = ['city', 'state']
 search_fields = ['firstName', 'lastName', 'addressOne', 'addressTwo','zipCode','city', 'state']