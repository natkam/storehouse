from django.contrib import admin
from .models import Shelf, Transport, Load, Section

admin.site.register(Shelf)
admin.site.register(Load)
admin.site.register(Transport)
admin.site.register(Section)
