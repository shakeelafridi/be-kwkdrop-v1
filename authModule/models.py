from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, TextField
from django.utils import tree
from utilities.models import Role
from django.utils.timezone import datetime
from django.db.models import JSONField
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    first_name = models.TextField(default='', db_column='first_name')
    middle_name = models.TextField(default='', db_column='middle_name')
    last_name = models.TextField(default='', db_column='last_name')
    name = models.TextField(default='', db_column='name')
    address = models.TextField(default='', db_column='address')
    zip_code = models.TextField(default='', db_column='zip_code')
    lat = models.TextField(default='', db_column='lat')
    lng = models.TextField(default='', db_column='lng')
    phone_number = models.CharField(default='', max_length=20, db_column='phone_number')
    date_of_birth = models.CharField(default='', max_length=15, db_column='date_of_birth')
    is_seller = models.BooleanField(default=False, db_column='is_seller')
    is_buyer = models.BooleanField(default=False, db_column='is_buyer')
    is_driver = models.BooleanField(default=False, db_column='is_driver')
    profile_image_url = models.TextField(default="", db_column='profile_image_url')
    is_email_verified = models.BooleanField(default=False, db_column='is_email_verified')
    email_verification_token = models.TextField(default='')
    is_active = models.BooleanField(default=False, db_column='is_active')
    strip_customer_key = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'UserProfile'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'UserRole'


class User_Addresses(models.Model):
    lat = models.CharField(max_length=30, default="")
    lng = models.CharField(max_length=30, default="")
    title = models.CharField(max_length=50, default="Other")
    bussines_name = models.CharField(max_length=50, default='')
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    appartment = models.CharField(max_length=50, default='')
    delivery_instruction = models.TextField(default='')
    is_default = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

#expired model
# class Card_Details(models.Model):
#     card_number = models.CharField(max_length=19)
#     cvv = models.IntegerField()
#     billing_address = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class BankAccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=255)
    account_object = models.CharField(max_length=255)
    holder_type = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    routing_number = models.CharField(max_length=255)
    stripe_source_key = models.TextField(max_length=255)
    status = models.CharField(max_length=255, default='')
    is_bank_account_verified = models.BooleanField(default=False)


class ResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    verification_code = models.CharField(default='', max_length=6, db_column='verification_code')
    key_expires = models.DateTimeField(default=datetime.now, db_column='key_expires')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


#Tempory buyer until not verified its email(expired model)
class TempUser(models.Model):
    email = models.CharField(default='', max_length=50)
    verification_code = models.CharField(default='', max_length=6, db_column='verification_code')
    key_expires = models.DateTimeField(default=datetime.now, db_column='key_expires')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

class PhoneNumbers(models.Model):
    phone_number = models.CharField(default='', max_length=30, db_column='phone_number')
    verification_code = models.CharField(default='', max_length=6, db_column='verification_code')
    key_expires = models.DateTimeField(default=datetime.now, db_column='key_expires')
    is_verified = models.BooleanField(default=False, db_column='is_verified')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'PhoneNumbers'


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=False, db_column='role')
    social_security_number = models.TextField(default='', db_column='social_security_number')
    lat = models.TextField(default='', db_column='lat')
    lng = models.TextField(default='', db_column='lng')
    is_verified_from_checker = models.BooleanField(default=False, db_column='is_verified')
    auto_insurance_number = models.TextField(default='', db_column='auto_insurance_number')
    auto_insurance_expiry = models.DateField(blank=True, null=True, db_column="auto_insurance_expiry")
    is_active = models.BooleanField(default=False)
    is_active_taxi_and_delivery_role = models.BooleanField(default=False)
    review_in_star = models.FloatField(default=5.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'Driver'

class DriverRoles(models.Model):
    name = models.CharField(max_length=255, default='')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

class Driver_checker(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, null=False)
    checker_driver_id = models.TextField(default='', db_column='checker_driver_id')
    checker_report_id = models.TextField(default='', db_column='checker_report_id')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


class License(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, db_column='driver')
    license_state = models.TextField(default='', db_column='license_state')
    license_number = models.TextField(default='', db_column='license_number')
    license_exp_date = models.DateField(blank=True, null=True, db_column="license_exp_date")
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

class VehicleType(models.Model):
    type = models.CharField(max_length=50, default='')

class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, db_column='driver')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    vehicle_make = models.TextField(default='', db_column='vehicle_make')
    vehicle_number = models.TextField(default='', db_column='vehicle_number')
    vehicle_color = models.TextField(default='', db_column='vehicle_color')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'Vehicle'


# class Bank_card_detail(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     name_of_card = CharField(default='', max_length=30, db_column='name_of_card')
#     card_number = CharField(default='', max_length=30, db_column='card_number')
#     expiry_date = CharField(default='', max_length=30, db_column='expiry_date')
#     cvv_number = CharField(default='', max_length=3, db_column='cvv_number')
#     billing_address = TextField(default='', db_column='billing_address')
#     is_save = BooleanField(default=False, db_column='is_save')
#     created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

#     class Meta:
#         db_table = 'Bank_card_details'


class DriverRadiusSettings(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # check for current location or fixed
    is_current_location = models.BooleanField(default=False)
    lat = models.CharField(max_length=255,default="")
    lng = models.CharField(max_length=255,default="")
    radius = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, db_column='user')
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False, db_column='profile')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=False, db_column='role')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'Seller'


class Shop(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, db_column='seller')
    shop_name = models.TextField(default='', db_column='shop_name')
    shop_address = models.TextField(default='', db_column='shop_address')
    is_always_open = models.BooleanField(default=False, db_column='is_always_open')
    phone_number = models.TextField(default='', db_column='phone_number')
    lat = models.TextField(default='', db_column='lat')
    lng = models.TextField(default='', db_column='lng')
    week = JSONField(null=True)
    review_in_star = models.FloatField(default=5.0)
    image = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'Shop'


class SellerShopHour(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    day = models.TextField(default='', db_column='day')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'SellerShopHour'


class ShopHourTiming(models.Model):
    hour = models.ForeignKey(SellerShopHour, on_delete=models.CASCADE)
    is_open_24 = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

    class Meta:
        db_table = 'ShopHourTiming'


class Shop_images(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=False, db_column='shop')
    shop_image_url = models.TextField(default='', db_column='shop_image_url')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


class FCMDevices(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE, )
    fcm_token = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


class Notification(models.Model):
    user = models.ManyToManyField(User, related_name='notifications')
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='notifications', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
