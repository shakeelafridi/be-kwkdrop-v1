from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, TextField
from django.utils import tree
from utilities.models import Role
from authModule.models import *
from django.utils.timezone import datetime


#Model that use to save records of vendor of shop
class Vendor(models.Model):
    full_name = TextField(default='', db_column='full_name')
    email_address = TextField(default='', db_column='email_address')
    phone_number = TextField(default='', db_column='phone_number')
    company = TextField(default='', db_column='company')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    shop = models.ForeignKey(Shop, null=True,on_delete=models.CASCADE, db_column='shop')

#Model that store all the shop's product
class Shop_Product(models.Model):
    title = models.TextField(default='', db_column='title')
    description = models.TextField(default='', db_column='description')
    price = models.FloatField(default=0, db_column='price')
    sale_price = models.FloatField(default=0, db_column='sale_price')
    is_active = models.BooleanField(default=False, db_column='is_active')
    sku = models.TextField(default='', db_column='sku')
    barcode = models.TextField(default='', db_column='barcode')
    quantity = models.IntegerField(default=0, db_column='quantity')
    weight = models.FloatField(default='', db_column='weight')
    weight_unit = models.TextField(default='', db_column='weight_unit')
    tags = models.TextField(default='', db_column='tags')
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL, db_column='vendor')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, db_column='seller')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop')
    created_at = models.DateTimeField(auto_now_add=True,null=True, db_column='created_at')

#Model that is used to store the product category
class Shop_Product_Category(models.Model):
    name = TextField(default='', db_column='name')
    shop_product = models.ForeignKey(Shop_Product,null=True ,on_delete=models.CASCADE, db_column='shop_product')
    created_at = models.DateTimeField(auto_now_add=True,null=True,db_column='created_at')

#Model that is used to store the product type
class Shop_Product_Type(models.Model):
    name = TextField(default='', db_column='name')
    shop_product_category = models.ForeignKey(Shop_Product_Category,null=True, on_delete=models.SET_NULL, db_column='shop_product_category')
    created_at = models.DateTimeField(auto_now_add=True,null=True,db_column='created_at')

#Model that is used to store the product images link
class Shop_Product_Images(models.Model):
    image_link = models.TextField(default='', db_column='image_link')
    shop_product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE, db_column='shop_product')
    created_at = models.DateTimeField(auto_now_add=True, null=True,db_column='created_at')

#Model that is used to store the product variants
class Shop_Product_Variant(models.Model):
    name = models.TextField(default='', db_column='name')
    value = models.TextField(default='', db_column='value')
    price = models.FloatField(default=0, db_column='price')
    sale_price = models.FloatField(default=0, db_column='sale_price')
    sku = models.TextField(default='', db_column='sku')
    barcode = models.TextField(default='', db_column='barcode')
    quantity = models.IntegerField(default=0, db_column='quantity')
    shop_product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE,  db_column='shop_product')
    created_at = models.DateTimeField(auto_now_add=True, null=True,db_column='created_at')

#Model that is used to store the product variants images link
class Shop_Product_Variant_Images(models.Model):
    image_link = models.TextField(default='', db_column='image_link')
    shop_product_variant = models.ForeignKey(Shop_Product_Variant, on_delete=models.CASCADE, db_column='shop_product_variant')
    created_at = models.DateTimeField(auto_now_add=True ,null=True,db_column='created_at')

#Model which is use store the option names of variants
class Shop_Product_Variant_Option(models.Model):
    option_name = models.TextField(default='', db_column='option_name')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, db_column='seller')
    created_at = models.DateTimeField(auto_now_add=True, null=True,db_column='created_at')

#Model that stores options values of variants
class Shop_Product_Variant_Option_value(models.Model):
    option_value = models.TextField(default='', db_column='option_value')
    shop_product_variant_option = models.ForeignKey(Shop_Product_Variant_Option, on_delete=models.CASCADE, db_column='shop_product_variant_option')
    created_at = models.DateTimeField(auto_now_add=True,null=True,db_column='created_at')

#Model of Propane companies
class Propane_Company(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#Model that maintain prices of propane
class Propane_Price(models.Model):
    propane_company = models.ForeignKey(Propane_Company, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

#Model of Propane tanks
class Propane(models.Model):
    # PROPANE_CHOICES = (
    #     ('new', 'NEW'),
    #     ("exchange",'EXCHANGE'),
    #     ('upgrade', 'UPGRADE'),
    #     ('deposite','DEPOSITE'),
    # )

    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField(null=True)
    is_active = models.BooleanField(default=False)
    sku = models.CharField(max_length=80)
    quantity = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    weight_unit = models.CharField(max_length=20)
    propane_category = models.CharField(max_length=8, default='')
    tags = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    company = models.ForeignKey(Propane_Company, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

#Model that saves propane images
class Propane_Images(models.Model):
    image_url = models.TextField()
    propane = models.ForeignKey(Propane, on_delete=models.CASCADE)

#Delivery Model
class Delivery_Options(models.Model):
    name=models.CharField(null=True, blank=True,max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

#Main Order maintain model
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    service_fee = models.FloatField(default=0)
    delivery_fee = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    is_payment_procced = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(User_Addresses, on_delete=models.SET_NULL, null=True)
    delivery_type = models.ForeignKey(Delivery_Options, on_delete=models.CASCADE,null=True)
    order_status = models.CharField(max_length=20, default='')
    is_shops_accepted = models.BooleanField(default=True)
    is_drivers_accepted = models.BooleanField(default=False)
    driver_accepted_time = models.DateTimeField(default=datetime.now)#use this for when buyer try to cancel order
    created_at = models.DateTimeField(auto_now_add=True)


#Shop Order maintain model
class ShopOrder(models.Model):
    ORDER_STATUS = (
        ('pending', 'PENDING'),
        ("accepted",'ACCEPTED'),
        ('completed', 'COMPLETED'),
        ('cancelled','CANCELLED'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    sub_total_amount = models.FloatField(default=0)
    is_driver_accepted = models.BooleanField(default=False)
    is_shop_accepted = models.BooleanField(default=True)
    order_status = models.CharField(max_length=20, default='accepted' ,choices=ORDER_STATUS)
    cancelled_by = models.CharField(max_length=10, default='')
    created_at = models.DateTimeField(auto_now_add=True)

#Order items
class Order_Items(models.Model):
    #product
    product = models.ForeignKey(Shop_Product, null=True, on_delete=models.CASCADE, db_column='product')
    product_quantity = models.IntegerField(default=0, db_column='quantity')
    #propane
    propane = models.ForeignKey(Propane, on_delete=models.SET_NULL, null=True)
    propane_quantity = models.IntegerField(default=0)
    propane_state = models.CharField(max_length=255, default="")
    order = models.ForeignKey(ShopOrder, on_delete=models.CASCADE)
    item_status = models.CharField(default="to-do",max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')


class Delivery_Scheduling(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    schedule_time = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')
    complete_order=models.BooleanField(default=False)

    
class AssignOrderToDriverForAcceptence(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    is_order_accepted =  models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True)

class AssignOrderListToDriver(models.Model):
    assign_order = models.ForeignKey(AssignOrderToDriverForAcceptence, on_delete=models.CASCADE)
    order = models.ForeignKey(ShopOrder, on_delete=models.CASCADE, null=True)
    
#Door step Model(if buyer is not available drop order at door step and take pictures)
class OrderDoorStepDelivered(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    images = models.JSONField(null=True)

#product reviews models
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)
    review_in_star = models.FloatField()
    review_in_text = models.TextField(default='')
    is_anonymous_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')
    

#product reviews models
class PropaneReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    propane = models.ForeignKey(Propane, on_delete=models.CASCADE)
    review_in_star = models.FloatField()
    review_in_text = models.TextField(default='')
    is_anonymous_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')
    

#Coupons model
class Coupon(models.Model):
    name = models.CharField(max_length=50)
    bogo = models.CharField(max_length=100)
    descriptions = models.TextField(default='')
    secret_code = models.TextField()
    discount_in_percentage = models.FloatField()
    expiry_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    