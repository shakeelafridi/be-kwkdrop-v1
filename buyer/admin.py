from seller.models import Coupon
from django.contrib import admin
from .models import *

# Register your models here.


class AddToCartAttributes(admin.ModelAdmin):
    list_display = ('id','user' ,'shop', 'product', 'product_quantity')
    
class CouponAttr(admin.ModelAdmin):
    list_display = ('id', 'name')


# Register your models here.
admin.site.register(Add_to_cart, AddToCartAttributes)
admin.site.register(Coupon, CouponAttr)