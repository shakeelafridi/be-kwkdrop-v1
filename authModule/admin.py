from seller.admin import ProductTypeAttributes
from authModule import models
from django.contrib import admin
from .models import *

# Register your models here.


class ProfileAttributes(admin.ModelAdmin):
    list_display = ('id','user', 'name', 'is_active', 'address', 'lat', 'lng', 'phone_number','date_of_birth', 'is_seller', 'is_buyer', 'is_driver')

class UserRoleAttributes(admin.ModelAdmin):
    list_display = ('id','user', 'role', 'is_active')

class ResetPasswordAttributes(admin.ModelAdmin):
    list_display = ('id','user', 'verification_code', 'key_expires')

class DriverAttributes(admin.ModelAdmin):
    list_display = ('id','user', 'profile', 'role', 'social_security_number', 'lat', 'lng')
    
class DriverRolesAttributes(admin.ModelAdmin):
    list_display = ('id', 'name', 'driver')

class DriverCheckerAttributes(admin.ModelAdmin):
    list_display = ('id', 'driver', 'checker_driver_id', 'checker_report_id')

class LicenseAttributes(admin.ModelAdmin):
    list_display = ('id','driver', 'license_state', 'license_number','license_exp_date')

class VehicleAttributes(admin.ModelAdmin):
    list_display = ('id','driver', 'vehicle_type', 'vehicle_make', 'vehicle_number', 'vehicle_color')

class BankAttributes(admin.ModelAdmin):
    list_display = ('id','driver', 'name_of_card', 'card_number', 'expiry_date', 'cvv_number', 'billing_address', 'is_save')

class SellerAttributes(admin.ModelAdmin):
    list_display = ('id','user', 'profile', 'role')

class ShopsAttributes(admin.ModelAdmin):
    list_display = ('id','seller', 'shop_name', 'shop_address', 'is_always_open', 'lat', 'lng')

class PhoneNumbersAttributes(admin.ModelAdmin):
    list_display = ('id', 'verification_code', 'phone_number')

class ShopImagesAttributes(admin.ModelAdmin):
    list_display = ('shop', 'shop_image_url')

class FCMDevicesAttributes(admin.ModelAdmin):
    list_display = ('user','fcm_token')

class DriverRadiusSettingsAttributes(admin.ModelAdmin):
    list_display = ('driver', 'is_current_location','lat','lng')

class UserAddressesAttributes(admin.ModelAdmin):
    list_display = ('id', 'address', 'user')

# class Bank_card_detailAttributes(admin.ModelAdmin):
#     list_display = ('id','user')

admin.site.register(UserProfile, ProfileAttributes)
admin.site.register(UserRole, UserRoleAttributes)
admin.site.register(ResetPassword, ResetPasswordAttributes)
admin.site.register(Driver, DriverAttributes)
admin.site.register(DriverRoles, DriverRolesAttributes)
admin.site.register(License, LicenseAttributes)
admin.site.register(Vehicle, VehicleAttributes)
admin.site.register(Seller, SellerAttributes)
admin.site.register(Shop, ShopsAttributes)
admin.site.register(PhoneNumbers, PhoneNumbersAttributes)
admin.site.register(Shop_images, ShopImagesAttributes)
admin.site.register(Driver_checker, DriverCheckerAttributes)
admin.site.register(FCMDevices, FCMDevicesAttributes)
admin.site.register(DriverRadiusSettings, DriverRadiusSettingsAttributes)
admin.site.register(User_Addresses, UserAddressesAttributes)
# admin.site.register(Bank_card_detail,Bank_card_detailAttributes)