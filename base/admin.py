from django.contrib import admin
from .models import Message , Blog ,Resource
# Register your models here.
admin.site.register(Message)
admin.site.register(Blog)
admin.site.register(Resource)