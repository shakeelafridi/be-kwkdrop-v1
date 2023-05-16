from buyer.buyer_reusable_resources import get_order_eta, get_shop_order_eta
from payments.reuseable_resources import calculate_main_order_amount, calculate_shop_order_amount
from seller.reuselable_resources import get_shop_rates
from django.db.models import fields
from django.db.models.aggregates import Avg
from rest_framework.fields import SerializerMethodField
from twilio.http import request
from rest_framework import serializers
from seller.models import *
from authModule.models import * 

#Reuseable Serializers
#User profile serializer(Generic)
class GetBuyerProfileDetailsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, object):
        user_object = User.objects.get(id=object.user.id)
        return GetUserDetailsSerializer(user_object).data
    
    class Meta:
        model = UserProfile
        fields = ['user','name','phone_number','first_name','middle_name','last_name','profile_image_url']

#User serializer(Generic)
class GetUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

#Buyer profile for order
class GetBuyerProfileDetailsForOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name','phone_number','profile_image_url']


#start Order----------------------------
#Order serializer
class GetOrderDetailsSerializer(serializers.ModelSerializer):
    shops_order_instance = serializers.SerializerMethodField()
    buyer_data = serializers.SerializerMethodField()
    shipping_address_data = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    eta = serializers.SerializerMethodField()

    def get_buyer_data(self, object):
        return GetBuyerDetailsForOrderSerializer(object.buyer).data
    
    def get_shipping_address_data(self, object):
        return UserAddressSerializer(object.shipping_address).data
    
    def get_shops_order_instance(self, object):
        shop_order_instances = ShopOrder.objects.filter(order=object)
        return GetShopOrderSerializer(shop_order_instances, many=True).data
    
    def get_total_amount(self, object):
        grand_total = calculate_main_order_amount(object)
        return grand_total

    def get_eta(self, object):
        total_eta = get_order_eta(object)
        return total_eta

    class Meta:
        model = Order
        fields = ['id','total_amount','service_fee','delivery_fee','is_drivers_accepted',
                  'is_shops_accepted','delivery_type','order_status','eta','created_at','shipping_address_data',
                  'buyer_data','shops_order_instance']

#Get shop order intance serializer
class GetShopOrderSerializer(serializers.ModelSerializer):
    shop_data = serializers.SerializerMethodField()
    driver_data = serializers.SerializerMethodField()
    ordered_products_items = serializers.SerializerMethodField()
    ordered_propanes_items = serializers.SerializerMethodField()
    sub_total_amount = serializers.SerializerMethodField()
    eta = serializers.SerializerMethodField()
    
    def get_shop_data(self, object):
        return ShopSerializer(object.shop).data
    
    def get_driver_data(self, object):
        try:
            if object.driver:
                return DriverSerializer(object.driver).data
        except Exception as e:
            print(e)
    
    def get_ordered_products_items(self, object):
        item_objects = Order_Items.objects.filter(order=object,product__isnull=False)
        return GetProductsFromOrderItemSerializer(item_objects, many=True).data
    
    def get_ordered_propanes_items(self, object):
        item_objects = Order_Items.objects.filter(order=object,propane__isnull=False)
        return GetPropaneFromOrderItemSerializer(item_objects, many=True).data

    def get_sub_total_amount(self, object):
        total_amount = calculate_shop_order_amount(object)
        return total_amount
    
    def get_eta(self, object):
        total_eta = get_shop_order_eta(object)
        return total_eta
    
    class Meta:
        model = ShopOrder
        fields = ['id', 'sub_total_amount','is_driver_accepted','is_shop_accepted','order_status','eta',
                  'shop_data','driver_data','ordered_products_items','ordered_propanes_items']


#Get orders items
class GetProductsFromOrderItemSerializer(serializers.ModelSerializer):
    products_info = serializers.SerializerMethodField()

    def get_products_info(self, object):
        if object.product is not None:
            # products_objects = Shop_Product.objects.get(id=object.product.id)
            return GetProductDetailsForOrderSerializer(object.product).data
        
    class Meta:
        model = Order_Items
        fields = ['product_quantity','products_info']
        
class GetPropaneFromOrderItemSerializer(serializers.ModelSerializer):
    propane_info = serializers.SerializerMethodField()

    def get_propane_info(self, object):
        if object.propane is not None:
            # propane_objects = Propane.objects.get(id=object.propane.id)
            return GetPropaneDetailsForOrderSerializer(object.propane).data
        
    class Meta:
        model = Order_Items
        fields = ['propane_quantity','propane_state','propane_info']


#Product Serialzier
class GetProductDetailsForOrderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, object):
        image_object = Shop_Product_Images.objects.filter(shop_product=object).first()
        return GetProductImagesSerailizer(image_object).data
    
    class Meta:
        model = Shop_Product
        fields = ['id','title','image']

#Product images serializer
class GetProductImagesSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Shop_Product_Images
        fields = ['image_link']

#Propane Serializer
class GetPropaneDetailsForOrderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, object):
        image_object = Propane_Images.objects.filter(propane=object).first()
        return GetPropaneImagesSerailizer(image_object).data
    class Meta:
        model = Propane
        fields = ['id','title','image']

#Propane images serializer
class GetPropaneImagesSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Propane_Images
        fields = ['image_url']
#------------------end Order object


#-------------------start shop order list
#Get shop order intance serializer
class GetShopOrderListSerializer(serializers.ModelSerializer):
    buyer_data = serializers.SerializerMethodField()
    ordered_products_items = serializers.SerializerMethodField()
    ordered_propanes_items = serializers.SerializerMethodField()
    shipping_address_data = serializers.SerializerMethodField()
    shops_order_instance = SerializerMethodField()
    sub_total_amount = serializers.SerializerMethodField()
    eta = serializers.SerializerMethodField()
    
    
    def get_buyer_data(self, object):
        return GetBuyerDetailsForOrderSerializer(object.order.buyer).data
    
    def get_shipping_address_data(self, object):
        return UserAddressSerializer(object.order.shipping_address).data
    
    def get_ordered_products_items(self, object):
        item_objects = Order_Items.objects.filter(order=object,product__isnull=False)
        return GetProductsFromOrderItemSerializer(item_objects, many=True).data
    
    def get_ordered_propanes_items(self, object):
        item_objects = Order_Items.objects.filter(order=object,propane__isnull=False)
        return GetPropaneFromOrderItemSerializer(item_objects, many=True).data

    def get_shops_order_instance(self, object):
        try:
            return ShopSerializer(object.shop).data
        except:
            pass
    
    def get_sub_total_amount(self, object):
        total_amount = calculate_shop_order_amount(object)
        return total_amount
    
    def get_eta(self, object):
        total_eta = get_shop_order_eta(object)
        return total_eta
    
    class Meta:
        model = ShopOrder
        fields = ['order', 'id','sub_total_amount','is_driver_accepted','is_shop_accepted','created_at','order_status','eta',
                  'shipping_address_data','buyer_data','shops_order_instance','ordered_products_items','ordered_propanes_items']
#-------------------end shop order list





class GetBuyerDetailsForOrderSerializer(serializers.ModelSerializer):
    buyer_profile = serializers.SerializerMethodField()

    def get_buyer_profile(self, object):
        profile_object = UserProfile.objects.get(user=object)
        return GetBuyerProfileDetailsForOrderSerializer(profile_object).data
    class Meta:
        model = User
        fields = ['id','buyer_profile']


#User address manipulatoins serializer --start-->
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Addresses
        fields = ['id','is_default','lat','lng','title','address','city','state','zipcode','appartment']


class CustomeUserAddressSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    is_default = serializers.SerializerMethodField()

    def get_is_default(self, object_):
        if User_Addresses.objects.filter(user=object_['user'],title=object_['title'], is_default=True).exists():
            is_default = True
        else:
            is_default = False
        return is_default

    def get_addresses(self, object_):
        addresses_object = User_Addresses.objects.filter(user=object_['user'],title=object_['title'])
        return UserAddressSerializer(addresses_object,many=True).data
    
    class Meta:
        model = User_Addresses
        fields = ['title','is_default','addresses']
#User address manipulatoins serializer <--end--


#Shop serializer
class ShopSerializer(serializers.ModelSerializer):
    review_in_star = serializers.SerializerMethodField()
    
    def get_review_in_star(self, object):
        try:
           get_rates = get_shop_rates(object)
           return get_rates
        except Exception as e:
            print(e)
            return 5.00
    class Meta:
        model = Shop
        fields = ['id','shop_name','phone_number','shop_address','lat','lng','review_in_star','image']


#Driver serializer
class DriverSerializer(serializers.ModelSerializer):
    driver_profile = serializers.SerializerMethodField()
    driver_location = serializers.SerializerMethodField()
    vehicle_information = serializers.SerializerMethodField()
    review_in_star = serializers.SerializerMethodField()
    

    def get_driver_profile(self, object):
        # profile_object = UserProfile.objects.get(id=object.profile.id)
        return GetBuyerProfileDetailsForOrderSerializer(object.profile).data

    def get_driver_location(self, object):
        try:
            location_object = DriverRadiusSettings.objects.get(driver=object)
            return DriverRadiusSerialzer(location_object).data
        except Exception as e:
            print(e)
    
    def get_vehicle_information(self, object):
        try:
            vehicle_object = Vehicle.objects.get(driver=object)
            return VehicleSerializer(vehicle_object).data
        except Exception as e:
            print(e)
            
    def get_review_in_star(self, object):
        try:
            return round(float(object.review_in_star), 2)
        except Exception as e:
            print(e)

    class Meta:
        model = Driver
        fields = ['id','is_active','driver_profile','driver_location','vehicle_information','review_in_star']

#Driver profile serializer

class DriverRadiusSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DriverRadiusSettings
        fields = ['is_current_location','lat','lng','radius']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_make','vehicle_number','vehicle_color']


#Coupons serailzer
class GetCouponSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        



#start__________________order tracking
class GetOrderTrackingSerialzer(serializers.ModelSerializer):
    # shipping_address = serializers.SerializerMethodField()
    # shops_addresses = serializers.SerializerMethodField()
    driver_address = serializers.SerializerMethodField()
    
    
    # def get_shipping_address(self, object):
    #     return GetUserAddressForTrackingSerializer(object.shipping_address).data
    
    # def get_shops_addresses(self, object):
    #     # shops_ids = ShopOrder.objects.filter(order=object).values_list('shop__id', flat=True)
    #     # shop_ids = list(shops_ids)
    #     # shops = Shop.objects.filter(id__in=shop_ids)
        
    #     shopOrder = ShopOrder.objects.filter(order=object).first()
    #     return GetShopsAddressesForTrackingSerializer(shopOrder.shop).data
    
    def get_driver_address(self, object):
        shop_order = ShopOrder.objects.filter(order=object).first()
        try:
            location_object = DriverRadiusSettings.objects.get(driver=shop_order.driver)
            return GetDriverRadiusForTrackingSerialzer(location_object).data
        except:
            pass
    
    class Meta:
        model = Order
        fields = ['driver_address']


class GetShopsAddressesForTrackingSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Shop
        fields = ['lat', 'lng']
        

class GetUserAddressForTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Addresses
        fields = ['lat','lng']
    
class GetDriverRadiusForTrackingSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DriverRadiusSettings
        fields = ['lat','lng']
#__________________________end tracking