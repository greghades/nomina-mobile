from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser,Roles

# Register your models here.
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('id', "name", "last_name", "email", "date_joined")
    fieldsets = (
      ('Employee info', {
          'fields': ('username','email','password','name','last_name','code_employee','ine','rfc','nss','status','date_start','rol')
      }),
   )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Roles)
admin.site.unregister(Group)