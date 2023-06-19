from django.contrib import admin

from portal_library_api.models import LibraryAdmin, LibraryBooks

# Register your models here.

admin.site.register(LibraryAdmin)
admin.site.register(LibraryBooks)
