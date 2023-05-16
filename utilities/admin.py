from django.contrib import admin
from utilities.models import *

# Register your models here.

class TempProductBarcodeScannerAttributes(admin.ModelAdmin):
    list_display = ('id','barcode', 'title', 'product_img', 'category', 'type')

class KwkUseCaseAttr(admin.ModelAdmin):
    list_display = ('id','name')

class KwkCartConfgAttr(admin.ModelAdmin):
    list_display = ('id','tax_value', 'discount_value')
    
class kwkChargesStructureAttr(admin.ModelAdmin):
    list_display = ('id', 'service_charges_in_percentage', 'delivery_charges_per_kilometer')

admin.site.register(KwkUsecase, KwkUseCaseAttr)
admin.site.register(KwkCartConfigurations, KwkCartConfgAttr)
admin.site.register(Role)
admin.site.register(LogEntryForException)
admin.site.register(Temp_Product_Barcode_Scanner, TempProductBarcodeScannerAttributes)
admin.site.register(kwkChargesStructure, kwkChargesStructureAttr)