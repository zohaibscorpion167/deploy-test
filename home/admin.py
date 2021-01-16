from django.contrib import admin
from home.models import Contact
from import_export.admin import ImportExportModelAdmin



# Register your models here.


@admin.register(Contact)
class ContactDisplay(ImportExportModelAdmin,admin.ModelAdmin):
   list_display = ['name', 'email', 'phone']
   search_fields = ['email']
   list_filter = ['email']
   pass
