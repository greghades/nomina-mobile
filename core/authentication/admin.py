from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('id', "first_name", "last_name", "email", "date_joined")
    fieldsets = (
      ('Employee info', {
          'fields': ('username','password','name','last_name','code_employee','ine','rfc','nss','status','date_start')
      }),
   )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)