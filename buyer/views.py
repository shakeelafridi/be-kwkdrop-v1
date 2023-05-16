from driver.reuseable_resources import update_driver_lat_lng
from seller.reuselable_resources import notify_users_on_order_updates
from colorama.ansi import Fore
from driver.models import DriverEarning
from buyer.buyer_reusable_resources import get_data_in_list, get_variant, validate_review_product
from twilio.rest.api.v2010.account import message
from requests.sessions import default_headers
from utilities.models import KwkCartConfigurations, KwkUsecase
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from utilities.reuseableResources import *
from .models import *
from kwk.settings import *
from seller.models import *
from utilities.jwt import JWTClass
decorator_ = DecoratorHandler()
jwt_ = JWTClass()
from .serializer import CustomeUserAddressSerializer, GetCouponSerialzer, GetOrderDetailsSerializer, GetOrderTrackingSerialzer, UserAddressSerializer,GetBuyerProfileDetailsSerializer
#testing purpose only
import random
#Twilio
from twilio.rest import Client
#date and time
import pytz
utc = pytz.UTC
import datetime as dt
from dateutil import parser
import stripe
stripe.api_key = STRIP_SECRET_KEY
from rest_framework import status

# from utilities.amazon import Amazon
# from json import dump
# from os import name
# from django.core.checks import messages
# from utilities.models import Temp_Product_Barcode_Scanner
# from django.contrib.auth import authenticate

@decorator_.rest_api_call(allowed_method_list=['GET'],
                            is_authenticated=True, authentication_level=BUYER_ROLE)
def desktop(request):
    user_name=""
    order_notifications=0
    other_notifications=6
    cart_items_counter=0
    user_=request.user
    
    try:
        cart_items=Add_to_cart.objects.filter(user=user_)
        for item in cart_items:
            try:
                cart_items_counter+=int(item.product_quantity)
                cart_items_counter+=int(item.propane_quantity)
            except:
                pass
    except:
        pass
    
    try:
        user_profile_=UserProfile.objects.get(user=user_)
        user_name=user_profile_.name
    except:
        pass
    
    try:
        address_objects = User_Addresses.objects.filter(user=user_, is_default=True).last()
        address_ = address_objects.address
    except:
        address_ = ""
    
    try:
       order_notifications = Order.objects.filter(buyer=user_, order_status__in=progress_order_list).count()
    except Exception as e:
        print(e)

    return SuccessResponse(data={
        "user_name":user_name,
        "user_cart_items_counter":cart_items_counter,
        "order_notifications":order_notifications,
        "other_notifications":other_notifications,
        'user_address':address_
    }).return_response_object()

#Get buyer profile
@decorator_.rest_api_call(allowed_method_list=['GET'],
                         is_authenticated=True, authentication_level=BUYER_ROLE)
def get_profile(request):
    try:
        user_ = request.user
        user_profile_ = UserProfile.objects.get(user=user_)
        buyer_profile_serializer_ = GetBuyerProfileDetailsSerializer(user_profile_).data
        return SuccessResponse(data={
            'buyer_profile':buyer_profile_serializer_
        }).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='invalid user, try again.').return_response_object()

#Desktop
@decorator_.rest_api_call(allowed_method_list=['GET', 'POST'],
                         is_authenticated=True, authentication_level=BUYER_ROLE)
def buyer_address_manipulation(request):
    user_ = request.user
    response_message_ = ""
    if request.method == "POST":
        try:
            data = get_request_obj(request)
            title_ = data['title']
            lat_ = data['lat']
            lng_ = data['lng']
            address_ = data['address']
            if not validate_null_address(lat_, lng_, address_):
                return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                            message='required fields, lat, lng, address').return_response_object()
            try:
                User_Addresses.objects.filter(user=user_).update(is_default=False)
                User_Addresses.objects.create(user=user_, lat=lat_, lng=lng_, address=address_, title=title_)
                response_message_ = 'address created.'
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unabale to save record.').return_response_object()
        except:
            try:
                id_ = data['update_id']
                if Order.objects.filter(shipping_address__id = id_, order_status__in = [PENDING, PREPARED, ACCEPTED, DISPUTED, STARTED]).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unable to change during order.').return_response_object()
                lat_ = data['lat']
                lng_ = data['lng']
                address_ = data['address']
                if not validate_null_address(lat_, lng_, address_):
                    return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                            message='required fields, lat, lng, address').return_response_object()
                try:
                    bussines_name_ = data['bussines_name']
                except:
                    bussines_name_ = ''
                try:
                    appartment_ = data['appartment']
                except:
                    appartment_ = ''
                try:
                    delivery_instruction_ = data['delivery_instruction']
                except:
                    delivery_instruction_ = ''
                try:
                    User_Addresses.objects.filter(user=user_).update(is_default=False)
                    User_Addresses.objects.filter(id=id_).update(lat=lat_, lng=lng_, address=address_,bussines_name=bussines_name_,
                                                                    is_default=True,appartment=appartment_,
                                                                    delivery_instruction=delivery_instruction_)
                except:
                    response_message_ = 'unable to update records'
            except:
                try:
                    id_ = data['default_id']
                    User_Addresses.objects.filter(user=user_).update(is_default=False)
                    try:
                        User_Addresses.objects.filter(id=id_).update(is_default=True)
                    except:
                        response_message_ = 'unable to set records to default.'
                except:
                    try:
                        id_ = data['delete_id']
                        if Order.objects.filter(shipping_address__id = id_, order_status__in = [PENDING, PREPARED, ACCEPTED, DISPUTED, STARTED]).exists():
                            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unable to change during order.').return_response_object()
                        try:
                            User_Addresses.objects.filter(id=id_).delete()
                        except:
                            response_message_ = 'unable to delete records'
                    except:
                        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message='please provide valid data').return_response_object()
    else:
        response_message_ = 'records feteched.'
    address_objects = User_Addresses.objects.filter(user=user_, is_delete=False).order_by('-id')
    user_addresses_serializer_ = UserAddressSerializer(address_objects,many=True).data
    return SuccessResponse(data={'addresses':user_addresses_serializer_}, message=response_message_).return_response_object()


#Get Shops
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=BUYER_ROLE)
def get_shops_for_buyer(request):
    user_ = request.user
    results = validate_buyer(user_)
    try:
        try:
            user_address_ = User_Addresses.objects.get(user=user_, is_default=True)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='please set your address').return_response_object()
        lat=user_address_.lat
        lng=user_address_.lng
    except:
        lat=None
        lng=None
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()

    #feature required(nearby shops)
    getAllShops = Shop.objects.all()
    getShopsArray = get_shops_objects_within_distance(getAllShops,lat,lng)
    return SuccessResponse(data={"shops":getShopsArray}).return_response_object()


#Get Products of shops
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=BUYER_ROLE)
def get_products_for_buyer(request):
    user_ = request.user
    promotion_images = []
    feature_products = []
    product_category_list = []
    dairy_products = []
    frozen_products = []
        
    results = validate_buyer(user_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    try:
        try:
            user_address_ = User_Addresses.objects.get(user=user_, is_default=True)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='please set your address.').return_response_object()
        lat=user_address_.lat
        lng=user_address_.lng
    except:
        lat=None #if user does 
        lng=None
    
    
    data = get_request_obj(request)
    try:
        shop_id_ = data['shop_id']
        if not shop_id_:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Please fill all the values").return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message="please provid valid data.").return_response_object()


    
    try:
        shopObj = Shop.objects.get(id=shop_id_)
        get_products = Shop_Product.objects.filter(shop=shopObj, quantity__gt=0)
        if get_products is None:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='shop is empty').return_response_object()

        eta_time=get_ETA_buyer_seller(lat,lng,shopObj.lat,shopObj.lng)
        # if eta_time<30:
        #     eta_time=30
                
        feature_products = get_products_objects(get_products)
        for item in feature_products:
            item.update( {'eta':'ETA: '+ str(int(eta_time)) + ' mints'})
        product_category_list.append({'product_category':'feature_products','product_list':feature_products})
        dairy_products = get_products_objects(get_products)
        for item in dairy_products:
            item.update( {'eta':'ETA: '+ str(int(eta_time)) + ' mints'})
        product_category_list.append({'product_category':'dairy_products','product_list':dairy_products})
        frozen_products = get_products_objects(get_products)
        for item in frozen_products:
            item.update( {'eta':'ETA: '+ str(int(eta_time)) + ' mints'})
        product_category_list.append({'product_category':'frozen_products','product_list':frozen_products})
        
        promotion_images.append({'promotion_image':'https://blog.creatopy.com/wp-content/uploads/2018/09/13-sales-promotions-techniques-to-boost-your-sales.png'})
        promotion_images.append({'promotion_image':'https://blog.creatopy.com/wp-content/uploads/2018/09/13-sales-promotions-techniques-to-boost-your-sales.png'})
        promotion_images.append({'promotion_image':'https://blog.creatopy.com/wp-content/uploads/2018/09/13-sales-promotions-techniques-to-boost-your-sales.png'})

        
        try:
            coupons = Coupon.objects.all()
            coupon_data = GetCouponSerialzer(coupons, many=True).data
        except Exception as e:
            print(e)
        
        return SuccessResponse(data={
            "products":product_category_list,
            "promotion_images":promotion_images,
            "coupons":coupon_data,
            }).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='invalid shop').return_response_object()    

#Get Product details
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=BUYER_ROLE)
def product_details(request):
    user_ = request.user
    results = validate_buyer(user_)
    data = get_request_obj(request)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    try:
        variant_list = []
        productImgLink = []
        same_class_variant_list = []
        product_review_list = []
        product_id_ = data['product_id']
        try:
            product_object = Shop_Product.objects.get(id=product_id_)
            product_review_objects = ProductReview.objects.filter(product=product_object)
            for object in product_review_objects:
                name = get_email_first_part(object.user.username)
                product_review_list.append({'user_name':name,
                                        'comment':object.review_in_text,
                                        'video_link':'https://www.youtube.com/watch?v=EngW7tLk6R8',
                                        'image_link':'' ,
                                        'rate':float(object.review_in_star),
                                        'is_anonymous_review':object.is_anonymous_review})
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid product').return_response_object()
        try:
            disctant_variants = Shop_Product_Variant.objects.filter(shop_product=product_object).distinct('name')
            for distant_variant_obj in disctant_variants:
                get_same_name_variants = Shop_Product_Variant.objects.filter(shop_product=product_object, name=distant_variant_obj.name)
                for same_class_obj in get_same_name_variants:
                    variant_disc = get_variant(same_class_obj)
                    variant_list.append(variant_disc)
                same_class_variant_list.append({'variant_name':same_class_obj.name, 'variants_values':variant_list})
                variant_list = []
        except:
            pass
        try:
            productImagesObj = Shop_Product_Images.objects.filter(shop_product=product_object)
            for image_object in productImagesObj:
                productImgLink.append({"url":image_object.image_link})
        except Exception as e:
            print(e)
            
        product_disc = get_product(product_object)
        product_disc.update({'variants':same_class_variant_list,
                             'product_image_url':productImgLink
                             })
        return SuccessResponse(data={"products":product_disc, 'reviews':product_review_list}).return_response_object()
        
    except:
        try:
            propane_id_ = data['propane_id']
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='incorrect data').return_response_object()
        propane_review_list = []
        try:
            propane_object = Propane.objects.get(id=propane_id_)
            product_disc = get_propane_object(propane_object)
            propane_review_objects = PropaneReview.objects.filter(propane=propane_object)
            for object in propane_review_objects:
                name = get_email_first_part(object.user.username)
                propane_review_list.append({'user_name':name,
                                        'comment':object.review_in_text,
                                        'video_link':'https://www.youtube.com/watch?v=EngW7tLk6R8',
                                        'image_link':'' ,
                                        'rate':float(object.review_in_star),
                                        'is_anonymous_review':object.is_anonymous_review})
            return SuccessResponse(data={'propane':product_disc, 'reviews':propane_review_list}).return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message='data not found').return_response_object()

#Static propane category list
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=BUYER_ROLE)
def propane_suggested_list(request):
    propane_list = []
    # try:
    #     propane_objects = Propane.objects.all()
    #     propane_randome_object = random.choice(propane_objects)
    # except:
    #     return FailureResponse(status_code=BAD_REQUEST_CODE, message="unable to get propane").return_response_object()

    #Static data(testing purposes)
    
    # propane_list = get_propane_object(propane_randome_object)
    
        #Static data(testing purposes)
        
    
    
    try:
        # new_propane_object = Propane.objects.filter(propane_category=PROPANE_NEW, quantity__gte=1, is_active=True).last()
        propane_object = Propane.objects.filter(quantity__gte=1, is_active=True).last()
        extract_propane_object = get_propane_object_details_for_suggesionlist(propane_object, PROPANE_NEW)
        propane_list.append(extract_propane_object)
        extract_propane_object = get_propane_object_details_for_suggesionlist(propane_object, PROPANE_EXCHANGE)
        propane_list.append(extract_propane_object)
        extract_propane_object = get_propane_object_details_for_suggesionlist(propane_object, PROPANE_UPGRADE)
        propane_list.append(extract_propane_object)
        extract_propane_object = get_propane_object_details_for_suggesionlist(propane_object, PROPANE_DISPOSE)
        propane_list.append(extract_propane_object)
        return SuccessResponse(data={"propane_list":propane_list}).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="unexpected error, try again").return_response_object()

#Add to cart
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=BUYER_ROLE)
def buyer_add_to_cart(request):
    cart_items_counter=0
    user_obj = request.user
    results = validate_buyer(user_obj)
    data = get_request_obj(request)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    
    # buyerObj = results['buyerObj']
    try:
        shop_id_ = int(data['shop_id'])
        quantity_ = int(data['quantity'])
        response_quantity_ = quantity_
        try:
            shop_obj = Shop.objects.get(id=shop_id_)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message='invalid shop').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message='incorret data').return_response_object()
    
    try:
        product_id_ = data['product_id']
        try:
            product_obj = Shop_Product.objects.get(id=product_id_)
            if not int(product_obj.quantity) >= quantity_:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                         message='product out of stock.').return_response_object()
            try:
                get_cart_object = Add_to_cart.objects.get(shop=shop_obj, product=product_obj, user=user_obj)
                response_quantity_ = int(get_cart_object.product_quantity) + quantity_
                get_cart_object.product_quantity = int(get_cart_object.product_quantity) + quantity_
                get_cart_object.save()
            except:
                try:
                    Add_to_cart.objects.create(shop=shop_obj, product=product_obj, user=user_obj, product_quantity=quantity_)
                except:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                             message='unable to save data.').return_response_object()
            product_obj.quantity = int(product_obj.quantity) - quantity_
            product_obj.save()
            try:
                cart_items = Add_to_cart.objects.filter(user=user_obj)
                for item in cart_items:
                    try:
                        cart_items_counter+=int(item.product_quantity)
                        cart_items_counter+=int(item.propane_quantity)
                    except:
                        pass
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message="unable to count carts items").return_response_object()
            return SuccessResponse(data={
                                    'product_quantities':response_quantity_,
                                    'cart_items_counter':cart_items_counter
                                    }, message='data added to cart.').return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message='invalid product').return_response_object()
    
    except:
        try:
            propane_id_ = data['propane_id']
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="incorrect data.").return_response_object()
        try:
            propane_obj = Propane.objects.get(id=propane_id_)
            if not int(propane_obj.quantity) >= quantity_:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                         message='propane out of stock.').return_response_object()
            try:
                get_cart_object = Add_to_cart.objects.get(shop=shop_obj, propane=propane_obj, user=user_obj)
                try:
                    response_quantity_ = int(get_cart_object.propane_quantity) + quantity_
                    get_cart_object.propane_quantity = int(get_cart_object.propane_quantity) + quantity_
                    get_cart_object.save()
                except:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                             message='unable to update data.').return_response_object()
            except:
                try:
                    Add_to_cart.objects.create(shop=shop_obj, propane=propane_obj, user=user_obj, propane_quantity=quantity_)
                except:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                             message='unable to save data.').return_response_object()
            propane_obj.quantity = int(propane_obj.quantity) - quantity_
            propane_obj.save()
            try:
                cart_items = Add_to_cart.objects.filter(user=user_obj)
                for item in cart_items:
                        try:
                            cart_items_counter+=int(item.product_quantity)
                            cart_items_counter+=int(item.propane_quantity)
                        except:
                            pass
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message="unable to count cart items").return_response_object()
            return SuccessResponse(data={
                                        'propane_quantities':response_quantity_,
                                        'cart_items_counter':cart_items_counter
                                        }, message='data added to cart.').return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message='invalid propane').return_response_object()

#Get cart item
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=BUYER_ROLE)
def get_data_from_cart(request):
    delivery_fee=220
    service_fee=12
    grand_total=0
    user_ = request.user
    results = validate_buyer(user_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=results['response_message']).return_response_object()
    try:
        get_distinct_shops = Add_to_cart.objects.filter(user=user_).values('shop').distinct()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message="card is empty.").return_response_object()

    shopsArray=[]
    total_price =  0
    sub_total_price = 0
    count_items = 0
    for distinct_shop_object in get_distinct_shops:
        shop_total_price = 0
        shop_sub_total_price = 0
        product_list=[]
        propane_list=[]
        get_cart_objects_by_shop = Add_to_cart.objects.filter(shop=distinct_shop_object['shop'], user=user_)
        for cart_object in get_cart_objects_by_shop:
            count_items+=1
            try:
                productObj = Shop_Product.objects.get(id=cart_object.product.id)
                product_image_objects = Shop_Product_Images.objects.filter(shop_product=productObj).last()
                product_dict = {
                    'cart_id':cart_object.id,
                    'product_id':productObj.id,
                    'product_image':product_image_objects.image_link,
                    'product_name':productObj.title,
                    'product_sale_price':productObj.sale_price,
                    'product_price':productObj.price,
                    'quantity':cart_object.product_quantity
                    }
                # shop_total_price = shop_total_price + (cart_object.product_quantity*productObj.sale_price)
                if productObj.sale_price == 0:
                    shop_sub_total_price = shop_sub_total_price + (cart_object.product_quantity*productObj.price)
                elif productObj.sale_price > 0:
                    shop_sub_total_price = shop_sub_total_price + (cart_object.product_quantity*productObj.sale_price)
                product_list.append(product_dict)
            except:
                propane_object = Propane.objects.get(id=cart_object.propane.id)
                propane_dict = {
                    'cart_id':cart_object.id,
                    'product_id':propane_object.id,
                    'product_image':"https://www.dpsgas.co.uk/wp-content/uploads/cylinder_propane_3.jpg",
                    'product_name':propane_object.title,
                    'product_sale_price':0,
                    'product_price':propane_object.price,
                    'quantity':cart_object.propane_quantity
                    }
                propane_list.append(propane_dict)
                shop_sub_total_price = shop_sub_total_price + (cart_object.propane_quantity*propane_object.price)
        shopObj = Shop.objects.get(id=distinct_shop_object['shop'])
        shop_dict = {
            "shop_id":distinct_shop_object['shop'],
            "shop_name":shopObj.shop_name,
            'shop_sub_total_price':shop_sub_total_price,
            "products":product_list+propane_list,
            "ETA":"10 mints"
            }
        shopsArray.append(shop_dict)
        sub_total_price = sub_total_price + shop_sub_total_price
    
    try:
        tariff_name_obj = KwkUsecase.objects.get(name=DELIVERY)
        tarrif_obj = KwkCartConfigurations.objects.get(use_case = tariff_name_obj)
        delivery_fee = tarrif_obj.tax_value

        tariff_name_obj = KwkUsecase.objects.get(name=SERVICE)
        tarrif_obj = KwkCartConfigurations.objects.get(use_case = tariff_name_obj)
        service_fee = tarrif_obj.tax_value
    except:
        delivery_fee = 0
        service_fee = 0

    propane_objects = Propane.objects.all()[:5]
    if propane_objects is not None:
        propane_list = get_propane_objects(propane_objects)

    total_price = delivery_fee + service_fee + sub_total_price
    payment_dist = {
        'delivery_fee':delivery_fee,
        'service_fee':service_fee,
        'total_payment':total_price,
        'total_items':count_items,
        'sub_total_payment':sub_total_price
        }
    return SuccessResponse(data={"shops":shopsArray,
                                 'payment_details':payment_dist,
                                 'suggested_items':propane_list}).return_response_object()


#Qutick edit in cart
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=BUYER_ROLE)
def quick_edit_to_cart(request):
    user_ = request.user
    results = validate_buyer(user_)
    data = get_request_obj(request)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    
    cart_id_ = data['cart_id']
    quantity_ = data['quantity']
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Please fill all the values").return_response_object()
    
    if Add_to_cart.objects.filter(id=cart_id_).exists():
        cartObj = Add_to_cart.objects.get(id=cart_id_)
        if cartObj.product:
            cartObj.product_quantity = quantity_
        else:
            cartObj.propane_quantity = quantity_
        cartObj.save()
        return SuccessResponse(data={'quantity_updated':quantity_},message='cart updated').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='invalid cart item').return_response_object()

#Delete from cart
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=BUYER_ROLE)
def delete_item_from_cart(request):
    user_ = request.user
    results = validate_buyer(user_)
    data = get_request_obj(request)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    
    cart_id_ = data['cart_id']
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message="Please fill all the values").return_response_object()
    
    if Add_to_cart.objects.filter(id=cart_id_).exists():
        cartObj = Add_to_cart.objects.get(id=cart_id_)
        cartObj.delete()
        return SuccessResponse(message='cart deleted').return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='invalid cart item').return_response_object()



#Future Notes
''' When buying cart saved items, we have to check if the quantity is availble or not
    if quantity is available than reduce quantity
'''

@decorator_.rest_api_call(allowed_method_list=['GET', 'POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def search_products_and_shops(request):
    user_ = request.user
    try:
        try:
            user_addresses_=User_Addresses.objects.get(user=user_, is_default=True)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="please set you address").return_response_object()
        lat=user_addresses_.lat
        lng=user_addresses_.lng
    except:
        lat=None
        lng=None
        
    results = validate_buyer(user_) #check if buyer is exists and the role is active
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    try:
        search_query_ = request.GET['search_query']
    except:
        data = get_request_obj(request)
        search_query_ = data['search_query']
        try:
            order_id = int(data['order_id'])
            if not order_id:
                order_id = None
        except:
            order_id = None
    #search queries when order placed
    if order_id is not None:
        try:
            shop_list = []
            product_list = []
            #get shops id in list
            get_shops_objects = ShopOrder.objects.filter(order__id=order_id).values_list('shop')
            shop_id_list = get_data_in_list(get_shops_objects)
            
            product_objects = Shop_Product.objects.filter(shop__id__in=shop_id_list, title__icontains=search_query_)
            propane_objects = Propane.objects.filter(shop__id__in = shop_id_list, title__icontains=search_query_)
            if product_objects is not None:
                product_list = get_product_objects_within_distance(product_objects,lat,lng)
            
            if propane_objects is not None:
                propane_list = get_propane_objects_within_distance(propane_objects,lat,lng)

            return SuccessResponse(data={
                                    "shops":shop_list,
                                    'products':product_list+propane_list}).return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="please provide valid data").return_response_object()
    
    #search query when user on desktop
    shop_list = []
    product_list = []
    shop_objects = Shop.objects.filter(shop_name__icontains=search_query_)
    product_objects = Shop_Product.objects.filter(title__icontains=search_query_)
    propane_objects = Propane.objects.filter(title__icontains=search_query_).order_by('company__id')
    if shop_objects is not None:
        shop_list = get_shops_objects_within_distance(shop_objects,lat,lng)
    
    if product_objects is not None:
        product_list = get_product_objects_within_distance(product_objects,lat,lng)

    if propane_objects is not None:
        propane_list = get_propane_objects_within_distance(propane_objects,lat,lng)

    return SuccessResponse(data={
                            "shops":shop_list,
                            'products':product_list+propane_list}).return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def promo_code(request):
    try:
        data = get_request_obj(request)
        promo_code_ = data['promo_code']
        total_payment_ = data['total_payment']
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='please provide valid data').return_response_object()
    try:
        get_promo_by_name = KwkUsecase.objects.get(name=PROMO, code=promo_code_)
        get_promo_code_record = KwkCartConfigurations.objects.get(use_case=get_promo_by_name)
        total_payment_ = float(get_promo_code_record.tax_value)-float(total_payment_)
        payment_dist = {
        'total_payment':total_payment_,
        }
        return SuccessResponse(data={'payment_details':payment_dist},
                                message='congratulations, promo applied.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid promo code').return_response_object()

@decorator_.rest_api_call(allowed_method_list=["GET","POST"], is_authenticated=True, authentication_level=[BUYER_ROLE])
def delivery_addresses_manipulations(request):
    user_ = request.user
    response_message_ = ""
    if request.method == "POST":
        try:
            data = get_request_obj(request)
            title_ = data['title']
            lat_ = data['lat']
            lng_ = data['lng']
            address_ = data['address']
            try:
                User_Addresses.objects.filter(user=user_).update(is_default=False)
                User_Addresses.objects.create(user=user_, lat=lat_, lng=lng_, address=address_, title=title_)
                response_message_ = 'address created.'
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unabale to save record.').return_response_object()
        except:
            try:
                id_ = data['update_id']
                if Order.objects.filter(shipping_address__id = id_, order_status__in = [PENDING, PREPARED, ACCEPTED, DISPUTED, STARTED]).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unable to change during order.').return_response_object()
                lat_ = data['lat']
                lng_ = data['lng']
                address_ = data['address']
                try:
                    bussines_name_ = data['bussines_name']
                except:
                    bussines_name_ = ''
                try:
                    appartment_ = data['appartment']
                except:
                    appartment_ = ''
                try:
                    delivery_instruction_ = data['delivery_instruction']
                except:
                    delivery_instruction_ = ''
                try:
                    User_Addresses.objects.filter(user=user_).update(is_default=False)
                    User_Addresses.objects.filter(id=id_).update(lat=lat_, lng=lng_, address=address_,bussines_name=bussines_name_,
                                                                    is_default=True,appartment=appartment_,
                                                                    delivery_instruction=delivery_instruction_)
                except:
                    response_message_ = 'unable to update records'
            except:
                try:
                    id_ = data['default_id']
                    User_Addresses.objects.filter(user=user_).update(is_default=False)
                    try:
                        User_Addresses.objects.filter(id=id_).update(is_default=True)
                    except:
                        response_message_ = 'unable to set records to default.'
                except:
                    try:
                        id_ = data['delete_id']
                        if Order.objects.filter(shipping_address__id = id_, order_status__in = [PENDING, PREPARED, ACCEPTED, DISPUTED, STARTED]).exists():
                            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message='unable to change during order.').return_response_object()
                        try:
                            User_Addresses.objects.filter(id=id_).delete()
                        except:
                            response_message_ = 'unable to delete records'
                    except:
                        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message='please provide valid data').return_response_object()
    else:
        response_message_ = 'records feteched.'
    user_ = request.user                
    address_objects = User_Addresses.objects.filter(user=user_, is_delete=False).values('title','user').distinct()
    user_addresses_serializer_ = CustomeUserAddressSerializer(address_objects,many=True).data
    return SuccessResponse(data={'user_addresses':user_addresses_serializer_},
                                 message=response_message_).return_response_object()
    
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def delivery_options(request):
    delivery_options_list = []
    ETA_ = ''
    deliver_fee_ = 0.0
    delivery_options_objects_ = Delivery_Options.objects.all()
    for option_object in delivery_options_objects_:
        if SELF_PICKUP == option_object.name.upper().replace(" ", ""):
            #define ETA only
            ETA_ = '20 mints'
            deliver_fee_ = 0.0
        else:
            #define ETA and deliver fee for deliver now option
            ETA_ = '10 mints'
            
        delivery_options_list.append({
            'id' : option_object.id,
            'name' :  option_object.name,
            'delivery_fee' : deliver_fee_,
            "ETA" : ETA_
        })
    return SuccessResponse(data={'delivery_options':delivery_options_list}).return_response_object()


#get buyer order details
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_order_details(request):
    try:
        buyer_ = request.user
        data = get_request_obj(request)
        order_id_ = int(data['order_id'])
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    try:
        update_driver_lat_lng(order_id_)
        get_order_objects = Order.objects.get(id=order_id_)
        order_serializer_ = GetOrderDetailsSerializer(get_order_objects).data
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='no order found.').return_response_object()

#get charges structure .i.e. delivery fee and services charges
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True,
                          authentication_level=[BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE])
def get_delivery_and_service_fee(request):
    try:
        data = get_request_obj(request)
        shops = data['shops']
        buyer = request.user
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='please provide valid data.').return_response_object()
    try:
        try:
            user_addresses_=User_Addresses.objects.get(user=buyer, is_default=True)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="please set you address").return_response_object()
        lat=user_addresses_.lat
        lng=user_addresses_.lng
    except:
        lat=None
        lng=None
    
    try:
        product_ids_list = []
        shop_ids_list = []
        product_list = []
        try:
            for shop in shops:
                shop_ids_list.append(shop['shop_id'])
                for product in shop['products']:
                    print(product)
                    if product['category'].upper() == PRODUCT:
                        product_ids_list.append(product['id'])
        except Exception as e:
            print(e)
            
        print(product_ids_list)
        try:
            category_list_ = Shop_Product_Category.objects.filter(shop_product__id__in=product_ids_list).values_list('name', flat=True)
            category_list_ = list(category_list_)
            products_id = Shop_Product_Category.objects.filter(name__in=category_list_).values_list('shop_product__id', flat=True)
            products_ids = list(products_id)
            get_products = Shop_Product.objects.filter(id__in=products_id)
            if get_products is not None:
                product_list = get_product_objects_within_distance(get_products,lat,lng)
        except Exception as e:
            print(e)
        
        except Exception as e:
            print()
        delivery_fee, service_fee = get_delivery_and_service_charges(shops, buyer)
        return SuccessResponse(data={
            "delivery_fee": delivery_fee,
            "service_fee":service_fee,
            "products":product_list
            }).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='unexpected error, try again.').return_response_object()


#get completed orders        
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_orders_history(request):
    try:
        data = get_request_obj(request)
        order_status_ = data['order_status'].lower()
        if not order_status_ in buyer_order_list_status_for_history:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="invalid order status").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    buyer_ = request.user
    try:
        if order_status_ == PROGRESS:
            get_order_objects = Order.objects.filter(buyer=buyer_,order_status__in=progress_order_list).order_by('created_at').reverse()
        else:
            get_order_objects = Order.objects.filter(buyer=buyer_,order_status=order_status_).order_by('created_at').reverse()
        order_serializer_ = GetOrderDetailsSerializer(get_order_objects,many=True).data                    
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='no order found.').return_response_object()
        
#review product and its shop        
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def review_product(request):
    buyer_ = request.user
    try:
        data = get_request_obj(request)
        products = data['products']
        is_valid_response = validate_review_product(products)
        if not is_valid_response:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="invalid product view data").return_response_object()        
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    
    for product in products:
        category = product['category'].upper().strip()
        product_id = product['product']
        review_in_star = float(product['review_in_star'])
        review_in_text = product['review_in_text']
        is_anonymous_review = product['is_anonymous_review']
        if review_in_star > 0.0:
            if category == PRODUCT:
                try:
                    get_product = Shop_Product.objects.get(id=product_id)
                    get_product.shop.review_in_star = (get_product.shop.review_in_star+review_in_star)/2
                    get_product.shop.save()
                    ProductReview.objects.create(user=buyer_, review_in_star=review_in_star, review_in_text = review_in_text, 
                                                is_anonymous_review=is_anonymous_review,product=get_product)
                except Exception as e:
                    print(e)
            elif category == PROPANE:
                try:
                    get_propane = Propane.objects.get(id=product_id)
                    get_propane.shop.review_in_star = (get_propane.shop.review_in_star+review_in_star)/2
                    get_propane.shop.save()
                    PropaneReview.objects.create(user=buyer_, review_in_star=review_in_star,review_in_text = review_in_text,
                                                is_anonymous_review=is_anonymous_review,propane = get_propane)
                except Exception as e:
                    print(e)
    return SuccessResponse(message="thanks for your feedback.").return_response_object()


#Assign driver to order
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True,
                          authentication_level=[BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE])
def assign_driver(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        order_object = Order.objects.get(id=order_id)
        get_all_buyer_order_objects_ = ShopOrder.objects.filter(order=order_object)
        try:
            get_all_active_drivers_objects_ = Driver.objects.all() #filter(is_active = True)
            buyer_lat_ = order_object.shipping_address.lat
            buyer_lng_ = order_object.shipping_address.lng
            for active_driver_object in get_all_active_drivers_objects_:
                try:
                    is_assignable_order_to_driver_ = get_driver_objects_within_distance(active_driver_object,
                                                                                buyer_lat_ ,buyer_lng_)
                except Exception as e:
                    print(Fore.YELLOW, e, 'unable to assign some driver')
                #Assign orders to driver for acceptence
                if is_assignable_order_to_driver_:
                    assigned_object = AssignOrderToDriverForAcceptence.objects.create(driver=active_driver_object,
                                                                                    order=order_object)
                    for buyer_order_object in get_all_buyer_order_objects_:
                        AssignOrderListToDriver.objects.create(assign_order=assigned_object,order=buyer_order_object)
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unable to assign driver.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()


#get products for review
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_products_for_review(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        products_list = []
        shop_orders = ShopOrder.objects.filter(order__id=order_id)
        for shop_order_object in shop_orders:
            order_item_objects = Order_Items.objects.filter(order=shop_order_object)
            for order_item in order_item_objects:
                if order_item.product is not None:
                    product_image = Shop_Product_Images.objects.filter(shop_product=order_item.product).first()
                    if product_image is not None:
                        image = product_image.image_link
                    else:
                        image = ""
                    disc = {
                        "category" : "product",
                        "title" : order_item.product.title,
                        "product":order_item.product.id,
                        "image" : image
                    }
                elif order_item.propane is not None:
                    propane_image = Propane_Images.objects.filter(propane=order_item.propane).first()
                    if propane_image is not None:
                        image = product_image.image_url
                    else:
                        image = ""
                    disc = {
                        "category" : "propane",
                        "title" : order_item.propane.title,
                        "product":order_item.propane.id,
                        "image" : image
                    }
                products_list.append(disc)
            return SuccessResponse(data={'products':products_list},
                                   message="thanks for your feedback.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
        
#get suggest list accordence order items
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def suggest_items_during_order_modification(request):
    user_ = request.user
    try:
        user_addresses_=User_Addresses.objects.get(user=user_, is_default=True)
        lat=user_addresses_.lat
        lng=user_addresses_.lng
        if lat is None or lng is None:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="please set you address").return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="please set you address").return_response_object()
    try:
        product_id_list = []
        category_list = []
        shop_list = []
        
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        #get product id's from order
        order_item_objects = Order_Items.objects.filter(order__id=order_id).values_list('product')
        product_id_list = get_data_in_list(order_item_objects)
        
        #get shops id in list
        get_shops_objects = ShopOrder.objects.filter(order__id=order_id).values_list('shop')
        shop_list = get_data_in_list(get_shops_objects)
        
        #category the product categories from product category accordence product id's
        get_suggest_products_objects = Shop_Product_Category.objects.filter(shop_product__id__in=product_id_list).values_list('name')
        category_list = get_data_in_list(get_suggest_products_objects)
        
        #get the all products base on order products categories
        product_id_list = []
        get_category_product_objects = Shop_Product_Category.objects.filter(name__in = category_list, shop_product__shop__id__in = shop_list).values_list('shop_product')
        product_id_list = get_data_in_list(get_category_product_objects)
        
        product_objects = Shop_Product.objects.filter(id__in=product_id_list)
        propane_objects = Propane.objects.filter(shop__id__in = shop_list)
        if product_objects is not None:
            product_list = get_product_objects_within_distance(product_objects,lat,lng)
        
        if propane_objects is not None:
            propane_list = get_propane_objects_within_distance(propane_objects,lat,lng)

        return SuccessResponse(data={
                                'products':product_list+propane_list}).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
        
#add new item during order
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def add_new_item_in_order(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        product_category = data['category'].upper()
        product_id = int(data['product_id'])
        shop_id = int(data['shop_id'])
        product_quantity = int(data['product_quantity'])
        #validate if order is already started
        try:
            order_object = Order.objects.get(id=order_id)
            if not order_object.order_status in valid_list_for_new_item_in_order:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unable to get item at this stage of order.').return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invaid order.').return_response_object()
        
        shop_order_object = ShopOrder.objects.filter(order__id=order_id, shop__id = shop_id).last()
        if shop_order_object is None:
            return FailureResponse(status_code=PAGE_NOT_FOUND,
                                    message="invalid order.").return_response_object()
        if product_category == PRODUCT:
            try:
                product_object = Shop_Product.objects.get(id=product_id, quantity__gte=product_quantity)
                try:
                    Order_Items.objects.update_or_create(
                        product=product_object,order=shop_order_object,
                        defaults={'product_quantity': product_quantity},
                    )
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="failed to add item.").return_response_object()
                    
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="product out of stock.").return_response_object()
                
        elif product_category == PROPANE:
            try:
                propane_object = Propane.objects.get(id=product_id, quantity__gte=product_quantity)
                try: 
                    Order_Items.objects.update_or_create(
                        propane=propane_object,order=shop_order_object,
                        defaults={'propane_quantity': product_quantity},
                    )
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="failed to add item.").return_response_object()
                    
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="product out of stock.").return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="invalid product category.").return_response_object()
        try:
            message_title_ = "Order modified."
            message_body_ = "New item has been added in order #"+str(order_object.id)+"."
            notify_users_on_order_updates(order_object, message_title_, message_body_, users_roles=[DRIVER_ROLE, SELLER_ROLE])
        except Exception as e:
            print(e)
        return SuccessResponse(message='item added successfully.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                message="please provide valid data.").return_response_object()


#Tip to driver
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def tip_and_review_driver(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        tip = float(data['tip'])
        rating = float(data['rating'])
        tip_by_card = data['by_card']
        if rating > 5.0:
            return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                    message="rate should not greater than 5.0").return_response_object()
        try:
            shop_order_object = ShopOrder.objects.filter(order__id=order_id).last()
            order_object = shop_order_object.order
            driver_object = shop_order_object.driver
            driver_object.review_in_star = float(float(driver_object.review_in_star+rating)/2)
            driver_object.save()
            if tip_by_card:
                pass
            else:
                DriverEarning.objects.create(order=order_object, tip=tip, driver = driver_object)
            return SuccessResponse(message='thanks for you feedback.').return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message="unable to rate driver, try again.").return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="failed, please try agian.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data.").return_response_object()

#order tracking(temp)
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True,
                          authentication_level=[BUYER_ROLE, SELLER_ROLE, DRIVER_ROLE])
def order_tracking(request):
    try:
        data = get_request_obj(request)
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        address = GetOrderTrackingSerialzer(order).data
        return SuccessResponse(data=address).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message="unexpected error.").return_response_object()


#for develop purposes only
def execute_randome_query(request):
    try:
        return SuccessResponse(message='succesed.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="try again.").return_response_object()