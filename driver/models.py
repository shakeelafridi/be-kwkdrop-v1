from authModule.models import Driver
from seller.models import Order, ShopOrder
from django.db import models
# Create your models here.

class DriverEarning(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tip = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

