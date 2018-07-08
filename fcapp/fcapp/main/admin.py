from django.contrib import admin
from .mongo_models import Device, Tenant
# Register your models here.
admin.site.register([Device, Tenant])