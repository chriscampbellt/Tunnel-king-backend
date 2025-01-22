from django.contrib import admin

from .models import InteractionLog, Model, ModelVariant

# Register your models here.
admin.site.register(Model)
admin.site.register(ModelVariant)
admin.site.register(InteractionLog)
