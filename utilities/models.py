from django.db import models
from django.utils.timezone import datetime

class LogEntryForException(models.Model):
    url = models.TextField(default='', db_column='url')
    user_agent = models.TextField(default='', db_column='user_agent')
    ip_address = models.TextField(default='', db_column='ip_address')
    exception = models.TextField(null=False, db_column='exception')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return self.exception

    class Meta:
        db_table = 'LogEntryForException'


class Role(models.Model):
    name = models.CharField(max_length=32, db_column='name')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Role'


class Temp_Product_Barcode_Scanner(models.Model):
    barcode = models.TextField(default='', db_column='barcode')
    title = models.TextField(default='', db_column='title')
    product_img = models.TextField(default='', db_column='product_img')
    category = models.TextField(default='category', db_column='category')
    type = models.TextField(default='', db_column='type')
    created_at = models.DateTimeField(auto_now_add=True, null=True,db_column='created_at')

class USState(models.Model):
    name = models.TextField(default='', db_column='name')
    abbr = models.TextField(default='', db_column='abbr')
    created_at = models.DateTimeField(auto_now_add=True,null=True, db_column='created_at')

class KwkUsecase(models.Model):
    name = models.TextField(blank=True,null=True, db_column='name')
    code = models.CharField(max_length=15, default='')
    created_at = models.DateTimeField(auto_now_add=True,null=True, db_column='created_at')

class KwkCartConfigurations(models.Model):
    tax_value= models.FloatField(blank=True,null=True)
    discount_value=models.FloatField(blank=True,null=True)
    use_case=models.ForeignKey(KwkUsecase,blank=True,null=True,on_delete=models.CASCADE)
    
class kwkChargesStructure(models.Model):
    service_charges_in_percentage = models.FloatField()
    delivery_charges_per_kilometer = models.FloatField()
