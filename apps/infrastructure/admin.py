from django.contrib import admin

from .models import Infrastructure, Log, SecurityPolicy

# Register your models here.
admin.site.register(Infrastructure)
admin.site.register(Log)
admin.site.register(SecurityPolicy)
