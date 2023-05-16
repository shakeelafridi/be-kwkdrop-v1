from driver.models import DriverEarning
from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from buyer.serializer import GetOrderDetailsSerializer, GetShopOrderSerializer
from rest_framework import serializers
from seller.models import *
from authModule.models import *


class GetListOfAssignOrderToDriverForAcceptence(serializers.ModelSerializer):
    assigned_order = serializers.SerializerMethodField()
    
    def get_assigned_order(self, object):
        return GetOrderDetailsSerializer(object.order).data
        
    class Meta:
        model = AssignOrderToDriverForAcceptence
        fields = ['id','assigned_order']
        
class GetDriverEarningSerializers(serializers.ModelSerializer):
    total_earning = SerializerMethodField()
    
    def get_total_earning(self, object):
        return object.order.delivery_fee
    
    class Meta:
        model = DriverEarning
        fields = ['id','total_earning', 'driver', 'order', 'tip', 'status' ,'created_at']

# class GetListAssignOrderListToDriverSerializer(serializers.ModelSerializer):
#     orders = serializers.SerializerMethodField()
    
#     def get_orders(self, object):
#        return GetShopOrderSerializer(object.order).data
   
#     class Meta:
#         model = AssignOrderListToDriver
#         fields = ['id','orders']