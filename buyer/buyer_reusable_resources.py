from colorama.ansi import Fore
from utilities.constants import PRODUCT, PROPANE
from authModule.models import Shop
from seller.models import Propane, Shop_Product, Shop_Product_Variant_Images
from utilities.constants import *
from seller.models import *
from authModule.models import *
from .models import *
import datetime as dt



def get_variant(variant_object):
    variant_images_list = []
    try:
        variantsImagesObj = Shop_Product_Variant_Images.objects.filter(shop_product_variant=variant_object).first()
        variant_images_list.append({'url':variantsImagesObj.image_link})
    except:
        variant_images_list.append({'url':""})

    variant_disc = {
        'variant_id':variant_object.id,
        'product_id':variant_object.shop_product.id,
        'variant_name':variant_object.name,
        'variant_value':variant_object.value,
        'variant_price':variant_object.price,
        'variant_sale_price':variant_object.sale_price,
        'sku':variant_object.sku,
        'barcode':variant_object.barcode,
        'quantity':variant_object.quantity,
        'cart_quantity':0,
        'variant_ETA':'10 mints',
        'variant_rating':'5',
        'variant_images':variant_images_list
    }
    return variant_disc


def reiview_shops_and_product(shops):
    is_order_placing_failed = False
    failed_shops_list = []
    failed_products_list = []
    total_payment_ = 0
    
    for shop in shops:
        try:#validate shop
            shop_object = Shop.objects.get(id=int(shop['shop_id']))
            products = shop['products']
            failed_products_list = []
            #iterate all products and propanes of shop
            for product in products:
                product_category = product['category'].upper().strip()
                #validate product only
                if product_category == PRODUCT:
                    try:#validate if product is available
                        product_object = Shop_Product.objects.get(id=int(product['product_id']))
                        if int(product['quantity']) < 1:
                            is_order_placing_failed = True
                            failed_products_list.append({'category':product['category'],
                                            'product_id':product['product_id'],
                                            'status':'invalid quantity',
                                            })
                        #check available quantity
                        elif int(product_object.quantity) < int(product['quantity']):
                            is_order_placing_failed = True
                            failed_products_list.append({'category':product['category'],
                                            'product_id':product['product_id'],
                                            'status':'out of stock',
                                            })
                        
                        if product_object.sale_price == 0:
                            total_payment_+=(int(product['quantity'])*product_object.price)
                        elif product_object.sale_price > 0:
                            total_payment_+=(int(product['quantity'])*product_object.sale_price)
                    except Exception as e:
                        print(e)
                        is_order_placing_failed = True
                        failed_products_list.append({'category':product['category'],
                                        'product_id':product['product_id'],
                                        'status':'not found',
                                        })
                #validate propane only
                elif product_category == PROPANE:
                    try:#validate if product is available
                        propane_object = Propane.objects.get(id=int(product['product_id']))
                        if int(product['quantity']) < 1:
                            is_order_placing_failed = True
                            failed_products_list.append({'category':product['category'],
                                            'product_id':product['product_id'],
                                            'status':'invalid quantity',
                                            })
                        #check available quantity
                        elif int(propane_object.quantity) < int(product['quantity']):
                            is_order_placing_failed = True
                            failed_products_list.append({'category':product['category'],
                                            'product_id':product['product_id'],
                                            'status':'out of stock',
                                            })
                        total_payment_+=(int(product['quantity'])*propane_object.price)
                            
                    except Exception as e:
                        print(e)
                        is_order_placing_failed = True
                        failed_products_list.append({'category':product['category'],
                                        'product_id':product['product_id'],
                                        'status':'not found',
                                        })
                
            failed_shops_list.append({'shop_id':shop['shop_id'],
                                    'status':'found',
                                    'products':failed_products_list})
        except:
            is_order_placing_failed = True
            failed_shops_list.append({'shop_id':shop['shop_id'],
                                      'status':'not found',
                                      'products':failed_products_list})
    return is_order_placing_failed, failed_shops_list, total_payment_
   
   
def shops_and_product_structure_validation(shops):
    for shop in shops:
        try:
            int(shop['shop_id'])
            products = shop['products']
            for product in products:
                int(product['product_id'])
                int(product['quantity'])
                float(product['product_sale_price'])
                float(product['product_price'])
                product_category_ = str(product['category']).upper().strip()
                if (not product_category_ == PROPANE) and (not product_category_ == PRODUCT):
                    return False
                
                if product_category_ == PROPANE:
                    propane_state_ = str(product['sub_category']).lower().strip() #new/upgrade/dispose/exchange
                    print(propane_state_)
                    if not propane_state_ in propane_type_list:
                        return False
                    
        except Exception as e:
            print(e)
            return False
    return True

def validate_review_product(products):
    is_data_valid = True
    for product in products:
        try:
            category = product['category'].upper().strip()
            if (not category == PRODUCT) and (not category == PROPANE):
                is_data_valid = False
            int(product['product'])
            str(product['review_in_text'])
            review_in_star = float(product['review_in_star'])
            if review_in_star > 5:
                is_data_valid = False
        except Exception as e:
            print(e)
            is_data_valid = False
    return is_data_valid
        
def validate_orders(orders):
    is_valid = True
    for order in orders:
        try:
            int(order['order_id'])
        except Exception as e:
            is_valid = False
            print(e)
    return is_valid

#convert tuple data in list
def get_data_in_list(tuple_):
    item_list = []
    for category in tuple_:
        if category[0] is not None:
            item_list.append(category[0])
    item_list = list(dict.fromkeys(item_list))
    return item_list

#get order eta, between buyer, shops and driver
def get_order_eta(order):
    from utilities.reuseableResources import get_ETA_buyer_driver, get_ETA_buyer_seller
    eta_time = 0
    driver = None
    try:
        buyer_lat = order.shipping_address.lat
        buyer_lng = order.shipping_address.lng
        shop_orders = ShopOrder.objects.filter(order=order)
        for object in shop_orders:
            eta_time += int(get_ETA_buyer_seller(buyer_lat,buyer_lng,object.shop.lat,object.shop.lng))
            try:
                driver = object.driver
            except Exception as e:
                print(e)
        if driver:
            try:
                driver_loc = DriverRadiusSettings.objects.get(driver=driver)
                eta_time+=int(get_ETA_buyer_driver(buyer_lat,buyer_lng,driver_loc.lat,driver_loc.lng))
            except Exception as e:
                print(e)
        if eta_time > 60: #convert into hours
            eta_time = float(eta_time/60)
            eta_time = round(eta_time, 2)
            eta_time = str(str(eta_time) +' hours')
        else:
            eta_time = round(eta_time, 2)
            eta_time = str(str(eta_time) +' mints')
        return eta_time
    except Exception as e:
        print(e)
        return str(str(30) +' mints') # mints


#get shop order eta
def get_shop_order_eta(shop_order):
    from utilities.reuseableResources import get_ETA_buyer_driver, get_ETA_buyer_seller
    eta_time = 0
    try:
        shop_order = ShopOrder.objects.get(id=shop_order.id)
        buyer_lat = shop_order.order.shipping_address.lat
        buyer_lng = shop_order.order.shipping_address.lng
        eta_time += int(get_ETA_buyer_seller(buyer_lat,buyer_lng,shop_order.shop.lat,shop_order.shop.lng))
        try:
            driver = shop_order.driver
            driver_loc = DriverRadiusSettings.objects.get(driver=driver)
            eta_time+=int(get_ETA_buyer_driver(buyer_lat,buyer_lng,driver_loc.lat,driver_loc.lng))
        except Exception as e:
            print(e)
            eta_time+=10 #supposition if any error
    except Exception as e:
        print(e)
        return str(str(30) +' mints') # mints
    if eta_time > 60: #convert into hours
        eta_time = float(eta_time/60)
        eta_time = round(eta_time, 2)
        eta_time = str(str(eta_time) +' hours')
    else:
        eta_time = round(eta_time, 2)
        eta_time = str(str(eta_time) +' mints')
    return eta_time
    
#assign order to drivers for acceptence
def assign_drivers_to_order(order):
    from utilities.reuseableResources import get_driver_objects_within_distance, notify_multiple_users
    driver_list = []
    try:
        order_id = order.id
        order_object = Order.objects.get(id=order_id)
        get_all_buyer_order_objects_ = ShopOrder.objects.filter(order=order_object)
        get_all_active_drivers_objects_ = Driver.objects.all() #filter(is_active = True)
        buyer_lat_ = order_object.shipping_address.lat
        buyer_lng_ = order_object.shipping_address.lng
        for active_driver_object in get_all_active_drivers_objects_:
            try:
                is_assignable_order_to_driver_ = get_driver_objects_within_distance(active_driver_object,
                                                                            buyer_lat_ ,buyer_lng_)
                if is_assignable_order_to_driver_:
                    assigned_object = AssignOrderToDriverForAcceptence.objects.create(driver=active_driver_object,
                                                                                    order=order_object)
                    for buyer_order_object in get_all_buyer_order_objects_:
                        AssignOrderListToDriver.objects.create(assign_order=assigned_object,order=buyer_order_object)
                    driver_list.append(active_driver_object.user)
            except Exception as e:
                print(Fore.YELLOW, e, 'unable to assign some driver')
            #Assign orders to driver for acceptence
        title = "New Job"
        body = "You have new order to accept."
        notify_multiple_users(driver_list, title, body)
    except Exception as e:
            print(e)
            
#promocode verification
def promocode_verification(promocode):
    from buyer.serializer import GetCouponSerialzer
    coupon_object = Coupon.objects.filter(secret_code=promocode, expiry_at__gte=dt.datetime.now()).last()
    if coupon_object is not None:
        serialized_obj = GetCouponSerialzer(coupon_object).data
        return True, serialized_obj
    return False, None