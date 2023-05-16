from authModule import models
from django.contrib import admin
from .models import *




class VendorAttributes(admin.ModelAdmin):
    list_display = ('id','full_name', 'email_address', 'phone_number', 'company', 'shop')

class ProductAttributes(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'is_active', 'sku', 'barcode','quantity','weight','weight_unit','tags','vendor','seller','shop')

class ProductTypeAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'shop_product_category')

class ProductCategoryAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'shop_product')

class ProductVariantAttributes(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'sale_price', 'sku', 'barcode','quantity','shop_product')

class ProductImagesAttributes(admin.ModelAdmin):
    list_display = ('id', 'image_link', 'shop_product')

class ProductVariantsImagesAttributes(admin.ModelAdmin):
    list_display = ('id', 'image_link', 'shop_product_variant')

class OptionsNameAttributes(admin.ModelAdmin):
    list_display = ('id', 'option_name','seller','shop')

class OptionsValuesAttributes(admin.ModelAdmin):
    list_display = ('id', 'option_value', 'shop_product_variant_option')

class PropaneCompanyAttributes(admin.ModelAdmin):
    list_display = ('id', 'name')

class PropanePricesAttributes(admin.ModelAdmin):
    list_display = ('id', 'propane_company', 'price')

class PropaneAttributes(admin.ModelAdmin):
    list_display = ('id','title','shop','seller','quantity')

class Delivery_OptionsAttributes(admin.ModelAdmin):
    list_display = ('id','name')
    
class Delivery_SchedulingAttributes(admin.ModelAdmin):
    list_display = ('id','order','schedule_time','complete_order')
    
class OrderAttributes(admin.ModelAdmin):
    list_display = ('id', 'order_status')

class ShopOrderAttributes(admin.ModelAdmin):
    list_display = ('id', 'shop')

class Order_ItemsAttributes(admin.ModelAdmin):
    list_display = ('id','product','product_quantity','propane','propane_quantity')
    
class AssignOrderToDriverForAcceptenceAttributes(admin.ModelAdmin):
    list_display = ('id','driver','order','is_order_accepted','created_at')

class AssignOrderListToDriverAttributes(admin.ModelAdmin):
    list_display = ('id', 'order')

# Register your models here.
admin.site.register(Vendor, VendorAttributes)
admin.site.register(ShopOrder, ShopOrderAttributes)
admin.site.register(Shop_Product_Type, ProductTypeAttributes)
admin.site.register(Shop_Product_Variant, ProductVariantAttributes)
admin.site.register(Shop_Product_Category, ProductCategoryAttributes)
admin.site.register(Shop_Product, ProductAttributes)
admin.site.register(Shop_Product_Images,ProductImagesAttributes)
admin.site.register(Shop_Product_Variant_Images, ProductVariantsImagesAttributes)
admin.site.register(Shop_Product_Variant_Option, OptionsNameAttributes)
admin.site.register(Shop_Product_Variant_Option_value, OptionsValuesAttributes)
admin.site.register(Propane_Company, PropaneCompanyAttributes)
admin.site.register(Propane_Price, PropanePricesAttributes)
admin.site.register(Propane, PropaneAttributes)
admin.site.register(Order, OrderAttributes)
admin.site.register(Order_Items, Order_ItemsAttributes)
admin.site.register(AssignOrderToDriverForAcceptence, AssignOrderToDriverForAcceptenceAttributes)
admin.site.register(Delivery_Options, Delivery_OptionsAttributes)
admin.site.register(Delivery_Scheduling, Delivery_SchedulingAttributes)
admin.site.register(AssignOrderListToDriver, AssignOrderListToDriverAttributes)