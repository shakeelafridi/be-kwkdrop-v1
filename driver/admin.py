from driver.models import DriverEarning
from django.contrib import admin
from authModule.models import VehicleType
# Register your models here.

class DriverEarningAttributes(admin.ModelAdmin):
    list_display = ('id', 'order', 'driver')

class VehicleTypeAttributes(admin.ModelAdmin):
    list_display = ('id', 'type')

admin.site.register(VehicleType, VehicleTypeAttributes)
admin.site.register(DriverEarning, DriverEarningAttributes)