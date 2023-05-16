from utilities.constants import BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE
from django.db.models.aggregates import Avg
from utilities.amazon import Amazon
from seller.models import ProductReview, PropaneReview, ShopOrder, Shop_Product, Shop_Product_Variant


#from csv, valiate product i.e. duplication, not found 
def validate_product(rowParent,shopsObject):
    is_conflicted = False
    dict_ = {}
    
    if rowParent['Insert_Update_Delete'].upper().strip() == 'I':
        if Shop_Product.objects.filter(barcode=rowParent['Barcode'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Barcode already exists, try update the product",
                        "title" : rowParent['Title'],
                        "barcode" : rowParent['Barcode'],
                        "sku" : "",
                        "Variation" : rowParent['Variation']
                        }
            
        if Shop_Product.objects.filter(sku=rowParent['SKU'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Barcode already exists, try update the product",
                        "title" : rowParent['Title'],
                        "barcode" : "",
                        "sku" : rowParent['SKU'],
                        "Variation" : rowParent['Variation']
                        }
        
    elif rowParent['Insert_Update_Delete'].upper().strip() == 'U':
        if not Shop_Product.objects.filter(barcode=rowParent['Barcode'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Invalid Barcode, unable to update the product",
                        "title" : rowParent['Title'],
                        "barcode" : rowParent['Barcode'],
                        "sku" : "",
                        "Variation" : rowParent['Variation']
                        }
            
        if not Shop_Product.objects.filter(sku=rowParent['SKU'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Invalid SKU, unable to update the product",
                        "title" : rowParent['Title'],
                        "barcode" : "",
                        "sku" : rowParent['SKU'],
                        "Variation" : rowParent['Variation']
                        }
            
    elif rowParent['Insert_Update_Delete'].upper().strip() == 'D':
        if not Shop_Product.objects.filter(barcode=rowParent['Barcode'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Invalid Barcode, unable to delete the product",
                        "title" : rowParent['Title'],
                        "barcode" : rowParent['Barcode'],
                        "sku" : "",
                        "Variation" : rowParent['Variation']
                        }
        
        if not Shop_Product.objects.filter(sku=rowParent['SKU'], shop=shopsObject).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Invalid SKU, unable to delete the product",
                        "title" : rowParent['Title'],
                        "barcode" : "",
                        "sku" : rowParent['SKU'],
                        "Variation" : rowParent['Variation']
                        }
    return dict_, is_conflicted


#from csv, valiate variant i.e. duplication, not found 
def validate_variant(rowChild, product):
    is_conflicted = False
    dict_ = {}
    
    if rowChild['Insert_Update_Delete'].upper().strip() == 'I':
        if Shop_Product_Variant.objects.filter(barcode=rowChild['Barcode'], shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Barcode already exists, try update the variant",
                        "title" : rowChild['Title'],
                        "barcode" : rowChild['Barcode'],
                        "sku" : "",
                        "Variation" : rowChild['Variation']
                        }
        elif Shop_Product_Variant.objects.filter(sku=rowChild['SKU'], shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "SKU already exists, try update the variant",
                        "title" : rowChild['Title'],
                        "barcode" : "",
                        "sku" : rowChild['SKU'],
                        "Variation" : rowChild['Variation']
                        }
    
    elif rowChild['Insert_Update_Delete'].upper().strip() == 'U':
        if not Shop_Product_Variant.objects.filter(barcode=rowChild['Barcode'],shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Barcode does not exist, try add the variant",
                        "title" : rowChild['Title'],
                        "barcode" : rowChild['Barcode'],
                        "sku" : "",
                        "Variation" : rowChild['Variation']
                        }

        if not Shop_Product_Variant.objects.filter(sku=rowChild['SKU'],shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "SKU does not exist, try add the variant",
                        "title" : rowChild['Title'],
                        "barcode" : "",
                        "sku" : rowChild['SKU'],
                        "Variation" : rowChild['Variation']
                        }
    
    elif rowChild['Insert_Update_Delete'].upper().strip() == 'D':
        if not Shop_Product_Variant.objects.filter(barcode=rowChild['Barcode'], shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "Barcode does not exist, unable to delete variant",
                        "title" : rowChild['Title'],
                        "barcode" : rowChild['Barcode'],
                        "sku" : "",
                        "Variation" : rowChild['Variation']
                        }
        elif not Shop_Product_Variant.objects.filter(sku=rowChild['SKU'], shop_product=product).exists():
            is_conflicted = True
            dict_ = {
                        "response_status": "SKU does not exist, Unable to delete variant",
                        "title" : rowChild['Title'],
                        "barcode" : "",
                        "sku" : rowChild['SKU'],
                        "Variation" : rowChild['Variation']
                        }
                
    return dict_, is_conflicted

def upload_csv_to_aws(file, csv_path_and_file_name):
    ext = file.split('.')[-1]
    name = file.split('.')[0].replace(" ", "")
    imgUrl = Amazon().upload_to_aws(name,csv_path_and_file_name, ext)
    csv_url = "https://kwkdrop.s3-us-east-2.amazonaws.com/media/"+imgUrl
    print(csv_url)
    return csv_url


#is all shop prepared picked the order, if yes than update the main order status
def is_all_shop_order_status_matched(order, status):
    shops_orders = ShopOrder.objects.filter(order__id=order.id)
    for object in shops_orders:
        if not object.order_status == status:
            return False
    return True

#update all shop order status as main order
def update_shop_order_status(order, status):
    ShopOrder.objects.filter(order=order).update(order_status=status)
    # if is_all_shop_order_status_matched(order, status):
    #     order.order_status = status
    #     order.save()

#get shop rates
def get_shop_rates(shop):
    try:
        products_rate = 5.00
        propanes_rate = 5.00
        get_products_avg_rate = ProductReview.objects.filter(product__shop=shop).aggregate(average_rating=Avg('review_in_star'))
        get_propane_avg_rate = PropaneReview.objects.filter(propane__shop=shop).aggregate(average_rating=Avg('review_in_star'))
        if get_products_avg_rate['average_rating'] is not None:
            products_rate = round(float(get_products_avg_rate['average_rating']), 2)
            
        if get_propane_avg_rate['average_rating'] is not None:
            propanes_rate = round(float(get_propane_avg_rate['average_rating']), 2)

        total_rates = (products_rate+propanes_rate)/2
        return round(total_rates,2)
    except Exception as e:
        print(e)
        return 5.00

#notify buyer, driver, shop
def notify_users_on_order_updates(order, title, body, users_roles=None):
    from utilities.reuseableResources import notify_multiple_users
    if users_roles is None:
        return False
    user_list = []
    if DRIVER_ROLE in users_roles:
        shop_orders = ShopOrder.objects.filter(order=order).last()
        try:
            driver = shop_orders.driver.user
            user_list.append(driver)
            # notify_user(driver, title, body)
        except:
            pass
    if SELLER_ROLE in users_roles:
        shop_orders = ShopOrder.objects.filter(order=order)
        for object in shop_orders:
            shop_user = object.shop.seller.user
            user_list.append(shop_user)
            # notify_user(shop_user, title, body)
    if BUYER_ROLE in users_roles:
        buyer = order.buyer
        user_list.append(buyer)
        # notify_user(buyer, title, body)
    notify_multiple_users(user_list, title, body)
    