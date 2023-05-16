from seller.models import Coupon, Order, Propane, Shop_Product
from authModule.models import Shop
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, CharField, TextField
from django.db.models.fields.related import ForeignKey

class Add_to_cart(models.Model):
    shop = models.ForeignKey(Shop, null=True, on_delete=models.CASCADE, db_column='shop')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_column='user')
    product = models.ForeignKey(Shop_Product, null=True, on_delete=models.CASCADE, db_column='product')
    product_quantity = models.IntegerField(default=0, db_column='quantity')
    propane = models.ForeignKey(Propane, on_delete=models.SET_NULL, null=True)
    propane_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')

#applied coupons
class BuyerAppliedCoupon(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_column='created_at')
    