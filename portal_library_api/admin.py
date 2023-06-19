from django.contrib import admin

from portal_library_api.models import Genre, LibraryAdmin, LibraryBooks

# Register your models here.

admin.site.register(LibraryAdmin)
admin.site.register(LibraryBooks)
admin.site.register(Genre)
