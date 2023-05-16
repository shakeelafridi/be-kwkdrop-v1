from utilities.response_messages import *
from driver.models import DriverEarning
from payments.models import StripeOrderPaymentIntent
from payments.reuseable_resources import calculate_main_order_amount, calculate_penalty
from django.db.models.expressions import F
import datetime as dt
from kwk.settings import FIREBASE_DATABASE, STRIP_SECRET_KEY
import stripe
from seller.reuselable_resources import notify_users_on_order_updates, update_shop_order_status, validate_product, validate_variant
from django.db.models import Q
from django.core.checks import messages
from utilities.models import Temp_Product_Barcode_Scanner
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from utilities.reuseableResources import *
from utilities.constants import *
from .models import *
from utilities.jwt import JWTClass
import pandas as pd
from utilities.amazon import Amazon
from buyer.serializer import GetShopOrderListSerializer
decorator_ = DecoratorHandler()
jwt_ = JWTClass()
stripe.api_key = STRIP_SECRET_KEY
from colorama import Fore
import pytz
utc = pytz.UTC
from dateutil import parser

#Add Vendor
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def add_vendor(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    full_name_ = data['full_name']
    email_address_ = data['email_address']
    phone_number_ = data['phone_number']
    company_ = data['company']
    role_ = data['role']
    shop_id_ = data['shop_id']

    userObj = request.user

    if role_.upper().strip() != "VENDOR":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()
    else:
        try:
            sellerObj = Seller.objects.get(user=userObj)
            if Shop.objects.filter(id=shop_id_,seller=sellerObj).exists():
                shopObj = Shop.objects.get(id=shop_id_)
                Vendor.objects.create(full_name=full_name_, email_address=email_address_, phone_number=phone_number_, company=company_, shop=shopObj)
                return SuccessResponse(message=SUCCESS_CREATED).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_SELLER_FOR_REQUESTED_SHOP).return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_FOUND).return_response_object()


#Update Vendor
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def update_vendor(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    full_name_ = data['full_name']
    email_address_ = data['email_address']
    phone_number_ = data['phone_number']
    company_ = data['company']
    role_ = data['role']
    shop_id_ = data['shop_id']
    vendor_id_ = data['vendor_id']

    userObj = request.user

    if role_.upper().strip() != "VENDOR":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()
    else:
        if Seller.objects.filter(user = userObj).exists():
            sellerObj = Seller.objects.get(user=userObj)
            if Shop.objects.filter(id=shop_id_,seller=sellerObj).exists():
                shopObj = Shop.objects.get(id=shop_id_)
                if Vendor.objects.filter(shop=shopObj, id=vendor_id_):
                    vendorObj =  Vendor.objects.get(id=vendor_id_)
                    vendorObj.full_name = full_name_
                    vendorObj.email_address = email_address_
                    vendorObj.phone_number = phone_number_
                    vendorObj.company = company_
                    vendorObj.save()
                    return SuccessResponse(message=SUCCESS_UPDATED).return_response_object()
                else:
                    return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_VENDOR_FOR_REQUESTED_SHOP).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_SELLER_FOR_REQUESTED_SHOP).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_FOUND).return_response_object()


#Delete Vendor
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def delete_vendor(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    role_ = data['role']
    shop_id_ = data['shop_id']
    vendors_ =data['vendors']
    if request.POST:
        vendors_ = json.loads(vendors_)

    userObj = request.user
    if role_.upper().strip() != SELLER_ROLE:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()
    else:
        if Seller.objects.filter(user = userObj).exists():
            sellerObj = Seller.objects.get(user=userObj)
            if Shop.objects.filter(id=shop_id_,seller=sellerObj).exists():
                shopObj = Shop.objects.get(id=shop_id_)
                for i in range(len(vendors_)):
                    if Vendor.objects.filter(shop=shopObj, id=vendors_[i]['vendor_id']).exists():
                        vendorObj =  Vendor.objects.get(id=vendors_[i]['vendor_id'])
                        vendorObj.delete()
                    else:
                        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_VENDOR_FOR_REQUESTED_SHOP).return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_SELLER_FOR_REQUESTED_SHOP).return_response_object()
            return SuccessResponse(message=SUCCESS_DELETED).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_FOUND).return_response_object()

#Show Vendor
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def show_vendor(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    shop_id_ = data['shop_id']
    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']
    venderObjects = Vendor.objects.filter(shop=shopsObject)
    vendors = []
    for obj in venderObjects:
        dict_ = {
                'id': obj.id,
                'vendor_name': obj.full_name,
                'phone_number':obj.phone_number,
                'email':obj.email_address,
                'company':obj.company
                }
        vendors.append(dict_)
    return SuccessResponse(data={'vendors': vendors}).return_response_object()


#Get shops for current seller
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[SELLER_ROLE])
def seller_desktop(request):
    order_notifications_ = 0
    other_notifications_ = 2
    try:
        user_ = request.user
        user_profile = UserProfile.objects.get(user=user_)
        if not user_profile.is_seller:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message=SELLER_NOT_ACTIVE).return_response_object()
        shops_ = Shop.objects.filter(seller__user=user_)
        full_name = user_profile.name
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_USER).return_response_object()
    shop_list = []
    for shop_ in shops_:
        shop_images_object_ = Shop_images.objects.filter(shop=shop_).last()
        if shop_images_object_ is not None:
            shop_image_url_ = shop_images_object_.shop_image_url
        else:
            shop_image_url_ = ""
        dict_ = {
            'id': shop_.id,
            'shop_name': shop_.shop_name,
            'shop_address': shop_.shop_address,
            'shop_image_link':shop_image_url_
        }
        shop_list.append(dict_)
        
    #count orders in progress
    try:
       order_notifications_ = ShopOrder.objects.filter(shop__seller__user=user_, order__order_status__in=progress_order_list).count()
    except Exception as e:
        print(e)

    return SuccessResponse(data={
        'full_name': full_name,
        'shops': shop_list,
        'order_notifications':order_notifications_,
        'other_notifications':other_notifications_
    }).return_response_object()


#Get the current login seller and shop details and also get the product category and type details
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_shop_seller_vendor_product_detais_for_add_product(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    shop_id_ = data['shop_id']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']

    venderObjects = Vendor.objects.filter(shop=shopsObject)
    vendors = []
    for obj in venderObjects:
        dict_ = {'id': obj.id, 'vendor_name': obj.full_name}
        vendors.append(dict_)
    product_dict_ = {
        "product_category":"shoes",
        "types": 
                [
                    {"product_type":"shoesTyp1"},
                    {"product_type":"shoesTyp2"},
                    {"product_type":"shoesTyp2"},
                ]
    }
    products = []
    products.append(product_dict_)
    product_dict_ = {
        "product_category":"cloths",
        "types": 
                [
                    {"product_type":"clothsTyp1"},
                    {"product_type":"clothsTyp2"},
                    {"product_type":"clothsTyp2"},
                ]
    }
    products.append(product_dict_)
    product_dict_ = {
        "product_category":"groceries",
        "types": 
                [
                    {"product_type":"fruits"},
                    {"product_type":"vegetables"},
                    {"product_type":"foods"},
                ]
    }
    products.append(product_dict_)
    product_dict_ = {
        "product_category":"furniture",
        "types": 
                [
                    {"product_type":"table"},
                    {"product_type":"chair"},
                    {"product_type":"bed"},
                ]
    }
    products.append(product_dict_)
    product_dict_ = {
        "product_category":"technology",
        "types": 
                [
                    {"product_type":"mobile"},
                    {"product_type":"tablet"},
                    {"product_type":"laptop"},
                ]
    }
    products.append(product_dict_)
    return SuccessResponse(data={'vendors': vendors, 'products_details':products}).return_response_object()


#Add Product in shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def add_Product_in_shop(request):
    data = get_request_obj(request)
    try:
        shop_id_ = data['shop_id']
        vendor_id_ = data['vendor_id']
        vendor_name_ = data['vendor_name']
        
        #product attributes
        title_ = data['title']
        description_ = data['description']
        price_ = float(data['price'])
        sale_price_ = float(data['sale_price'])
        is_active_ = data['is_active']
        sku_ = data['sku']
        barcode_ = data['barcode']
        quantity_ = int(data['quantity'])
        weight_ = data['weight']
        weight_unit_ = data['weight_unit']
        tags_ = data['tags']
        product_category_ = data['product_category']
        product_type_ = data['product_type']
        product_images_ = data['product_images']
        variants_ = data['variants']
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=PROVIDE_VALID_DATA).return_response_object()
    if not price_ > sale_price_:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=SALE_PRICE_GREATER_CONFLICT).return_response_object()
    if request.POST:
        variants_ = json.loads(variants_)

    userObj = request.user
    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    sellerObj = results['sellerObj']
    shopsObject = results['shopObj']
    if request.POST:
        product_images_ = json.loads(product_images_)

    if vendor_id_=="null" or vendor_id_ == "" or vendor_id_ == None:
        createVendorObj = Vendor.objects.create(full_name=vendor_name_, shop=shopsObject)
        vendor_id_=createVendorObj.id

    if Vendor.objects.filter(id=vendor_id_, shop=shopsObject).exists():
        vendorObj = Vendor.objects.get(id=vendor_id_)
        if Shop_Product.objects.filter(barcode=barcode_, shop=shopsObject, seller=sellerObj).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=BARCODE_ALREADY_EXISTS).return_response_object()

        if Shop_Product.objects.filter(sku=sku_, shop=shopsObject, seller=sellerObj).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=SKU_ALREADY_EXISTS).return_response_object()

        productObj = Shop_Product.objects.create(
                                                    title = title_,
                                                    description = description_,
                                                    price = price_,
                                                    sale_price = sale_price_,
                                                    is_active = is_active_,
                                                    sku = sku_,
                                                    barcode = barcode_,
                                                    quantity = quantity_,
                                                    weight = weight_,
                                                    weight_unit = weight_unit_,
                                                    tags = tags_,
                                                    vendor = vendorObj,
                                                    shop = shopsObject,
                                                    seller = sellerObj
                    )
        categoryObj = Shop_Product_Category.objects.create(name=product_category_, shop_product=productObj)
        Shop_Product_Type.objects.create(name=product_type_, shop_product_category = categoryObj)

        
        # #Upload Image
        for i in range(len(product_images_)):
            imgUrl = product_images_[i]['url']
            Shop_Product_Images.objects.create(image_link=imgUrl, shop_product=productObj)
        for i in range(len(variants_)):
            variant_name = variants_[i]['variant_name']
            variant_value = variants_[i]['variant_value']
            variant_price = variants_[i]['variant_price']
            variant_sale_price = variants_[i]['variant_sale_price']
            variant_sku = variants_[i]['variant_sku']
            variant_barcode = variants_[i]['variant_barcode']
            variant_quantity = variants_[i]['variant_quantity']
            variant_images = variants_[i]['variant_images']
            if request.POST:
                variant_images = json.loads(variant_images)
            variantObj =  Shop_Product_Variant.objects.create(
                name = variant_name,
                value = variant_value,
                price = variant_price,
                sale_price = variant_sale_price,
                sku = variant_sku,
                barcode = variant_barcode,
                quantity = variant_quantity,
                shop_product = productObj,
            )
            for j in range(len(variant_images)):
                variant_img_link = variant_images[j]['url']
                Shop_Product_Variant_Images.objects.create(image_link=variant_img_link, shop_product_variant=variantObj)
        return SuccessResponse(message=SUCCESS_CREATED).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_VENDOR_FOR_REQUESTED_SHOP).return_response_object()


#Product Image upload to AWS
@decorator_.rest_api_call(allowed_method_list=['POST'])
def upload_image_to_aws_and_get_link(request):
    product_images_urls = []
    #Upload Image
    if not request.FILES.getlist('upload_images_to_aws'):
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=PROVIDE_VALID_DATA).return_response_object()
        
    for product_img in request.FILES.getlist('upload_images_to_aws'):
        img = product_img
        ext = img.name.split('.')[-1]
        name = img.name.split('.')[0].replace(" ", "")
        imgUrl = Amazon().upload_to_aws(name,img, ext)
        product_images_urls.append({
            'url':"https://kwkdrop.s3-us-east-2.amazonaws.com/media/"+imgUrl
        })
    return SuccessResponse(data={
    'images_urls':product_images_urls,
    }).return_response_object()

#Delete Product from shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def delete_product_in_shop(request):
    data = get_request_obj(request)
    
    shop_id_ = data['shop_id']
    products = data['products']
    if request.POST:
        products = json.loads(products)
    userObj = request.user
    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    sellerObj = results['sellerObj']
    shopsObject = results['shopObj']

    for i in range(len(products)):
        if Shop_Product.objects.filter(id=products[i]['product_id'], shop=shopsObject, seller=sellerObj).exists():
            productObj = Shop_Product.objects.get(id=products[i]['product_id'], shop=shopsObject, seller=sellerObj)
            productObj.delete()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_PRODUCT_FOR_REQUESTED_SHOP).return_response_object()
    return SuccessResponse(message=SUCCESS_DELETED).return_response_object()

#Update Product of shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def update_product_in_shop(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    try:
        shop_id_ = data['shop_id']
        product_id_ = data['product_id']

        #Product's Attributes
        title_ = data['title']
        description_ = data['description']
        price_ = float(data['price'])
        sale_price_ = float(data['sale_price'])
        is_active_ = data['is_active']
        sku_ = data['sku']
        barcode_ = data['barcode']
        quantity_ = data['quantity']
        weight_ = data['weight']
        weight_unit_ = data['weight_unit']
        tags_ = data['tags']
        product_category_ = data['product_category']
        product_type_ = data['product_type']
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=PROVIDE_VALID_DATA).return_response_object()

    if not price_ > sale_price_:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=SALE_PRICE_GREATER_CONFLICT).return_response_object()

    userObj = request.user
    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    sellerObj = results['sellerObj']
    shopsObject = results['shopObj']

    if Shop_Product.objects.filter(id=product_id_, shop=shopsObject, seller=sellerObj).exists():
        productObj = Shop_Product.objects.get(id=product_id_, shop=shopsObject, seller=sellerObj)

        productObj.title = title_
        productObj.description = description_
        productObj.price = price_
        productObj.sale_price = sale_price_
        productObj.is_active = is_active_
        productObj.sku = sku_
        productObj.barcode = barcode_
        productObj.quantity = quantity_
        productObj.weight = weight_
        productObj.weight_unit = weight_unit_
        productObj.tags = tags_
        productObj.save()
        if Shop_Product_Category.objects.filter(shop_product=productObj).exists():
            categoryObj = categoryObj = Shop_Product_Category.objects.get(shop_product=productObj)
            categoryObj.name = product_category_
            categoryObj.save()
            if Shop_Product_Type.objects.filter(shop_product_category = categoryObj).exists():
                productTypeObj = Shop_Product_Type.objects.get(shop_product_category = categoryObj)
                productTypeObj.name = product_type_
                productTypeObj.save()
            else:
                Shop_Product_Type.objects.create(name=product_type_, shop_product_category=categoryObj)
        else:
            categoryObj = Shop_Product_Category.objects.create(name=product_category_, shop_product=productObj)
            Shop_Product_Type.objects.create(name=product_type_, shop_product_category=categoryObj)
        return SuccessResponse(message=SUCCESS_UPDATED).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_PRODUCT_FOR_REQUESTED_SHOP).return_response_object()


#Add Products and variatns from csv file
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True ,authentication_level=SELLER_ROLE)
def add_products_by_csv(request):

    conflicted_list = []
    failed_products = 0
    try:
        getFile = request.FILES['csv_file']
        csvData = pd.read_csv(getFile)
        csvData = csvData.drop([0])
        # total_products = len(csvData.index)
        parents = csvData.query('Variation == "parent"')
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=CSV_READING_FAILED).return_response_object()

    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    shop_id_ = data['shop_id']
    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    sellerObj = results['sellerObj']
    shopsObject = results['shopObj']

    total_products = 0
    for indexParent, rowParent in parents.iterrows():
        total_products+=1
        try:
            product_title = rowParent['Title']
            product_decs = rowParent['Description']
            product_price = float(rowParent['Price'].split("$")[1])
            product_sale_price = float(rowParent['Sale_Price'].split("$")[1])
            product_weight = rowParent['Weight']
            product_weight_unit = rowParent['Unit']
            product_sku = rowParent['SKU']
            product_barcode = rowParent['Barcode']
            product_quantity = rowParent['Quantity']
            product_category = rowParent['Category']
            product_type = rowParent['Type']
            product_vendor_name = rowParent['Vendor']
            product_tags = rowParent['Tags']
            product_status = rowParent['Status']
            option_name = rowParent['variation_theme']
            if not product_sale_price < product_price:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message=SALE_PRICE_GREATER_CONFLICT).return_response_object()
            if product_status.upper().strip() == "ACTIVE":
                product_is_active_ = True
            else:
                product_is_active_ = False
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message=CSV_PRODUCTS_READING_FAILED).return_response_object()
        
        response_data, is_conflicted = validate_product(rowParent, shopsObject)
        if is_conflicted:
            failed_products+=1
            conflicted_list.append(response_data)
            continue
            # return SuccessResponse(data=response_data).return_response_object()
        
        try:
            vendorObj, created = Vendor.objects.get_or_create(full_name=product_vendor_name, shop=shopsObject)
        except Exception as e:
            failed_products+=1
            print(e)
            continue
        
        if rowParent['Insert_Update_Delete'].upper().strip() == 'D':
            Shop_Product.objects.filter(barcode=product_barcode, sku=product_sku,
                                            shop=shopsObject,seller=sellerObj).delete()
            continue
                
        
        if rowParent['Insert_Update_Delete'].upper().strip() == 'I' or rowParent['Insert_Update_Delete'].upper().strip() == 'U':
            productObj, created = Shop_Product.objects.get_or_create(
                barcode = product_barcode,
                sku = product_sku,
                shop = shopsObject,
                defaults = {
                    'vendor' : vendorObj,
                    'is_active' : product_is_active_,
                    'title' : product_title,
                    'description' : product_decs,
                    'price' : product_price,
                    'sale_price' : product_sale_price,
                    'quantity' : product_quantity,
                    'weight' : product_weight,
                    'weight_unit' : product_weight_unit,
                    'tags' : product_tags,
                    'seller' : sellerObj
                }
            )

                
            categoryObj = Shop_Product_Category.objects.create(name=product_category, shop_product=productObj)
            Shop_Product_Type.objects.create(name=product_type, shop_product_category = categoryObj)
            for indexData, rowChild in csvData.iterrows():
                if rowParent["SKU"] == rowChild["parent_sku"]:
                    variant_response, is_variant_conflicted = validate_variant(rowChild, productObj)
                    if is_variant_conflicted:
                        failed_products+=1
                        conflicted_list.append(variant_response)
                        continue
                    
                    if rowChild['Insert_Update_Delete'].upper().strip() == 'D':
                        Shop_Product_Variant.objects.get(
                                    sku = rowChild["SKU"],
                                    barcode = rowChild["Barcode"],
                                    shop_product = productObj).delete()
                        continue
                    
                    Shop_Product_Variant.objects.get_or_create(
                                sku = rowChild["SKU"],
                                barcode = rowChild["Barcode"],
                                shop_product = productObj,
                                defaults = {
                                    'name' : option_name,
                                    'value' : rowChild["variation_theme"],
                                    'price' : rowChild["Price"].split("$")[1],
                                    'sale_price' : rowChild["Sale_Price"].split("$")[1],
                                    'quantity' : rowChild["Quantity"]
                                }
                            )

    # import os
    # from django.conf import settings

    # csv_files_path = 'utilities/products_csv_files/'
    # file_name = 'data.csv'
    # csv_path_and_file_name = str(str(csv_files_path)+str(file_name))
    # with open(csv_path_and_file_name, 'w', encoding='utf-8', newline='') as file:
    #     fieldnames = ['response_status', 'title', 'barcode', 'sku', 'Variation']
    #     writer = csv.DictWriter(file, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows(conflicted_list)
    
    # file_ = open(csv_files_path,'r')
    # print(file_.read())
    # csv_url = upload_csv_to_aws(file_name,file_)
    
    return SuccessResponse(data={
        'total_products':total_products,
        'failed_products' : failed_products,
        'failed_products_details':conflicted_list,
        'csv_url' :"https://kwkdrop.s3-us-east-2.amazonaws.com/media/KWK_seller_products_sample(1)-ohxnkrhjfyovhgtx-210804_084630-hglcigmemqkrrwkf-210804_085808.csv"
        }).return_response_object()



#Get Products of specific shop of specific seller
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_product_for_shop(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    shop_id_ = data['shop_id']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']
            
    getAllProducts = Shop_Product.objects.filter(shop=shopsObject)
    products = []
    for productObj in getAllProducts:
        if Shop_Product_Category.objects.filter(shop_product=productObj).exists():
            productCategoryObj = Shop_Product_Category.objects.get(shop_product=productObj)
            categoryName = productCategoryObj.name
        else:
            categoryName = ""
        if Shop_Product_Images.objects.filter(shop_product=productObj).exists():
            productImagesObj = Shop_Product_Images.objects.filter(shop_product=productObj).first()
            productImgLink = productImagesObj.image_link
        else:
            productImgLink = ""

        product_dict_ = {
                        'id':productObj.id,
                        'title':productObj.title,
                        'price':productObj.price,
                        'category':categoryName,
                        'is_active':productObj.is_active,
                        'quantity':productObj.quantity,
                        'product_image_link':productImgLink
                        }
        products.append(product_dict_)
    return SuccessResponse(data={'products_details':products}).return_response_object()


#Get Products scanning barcode
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_products_scanning_barcode(request):
    try:
        data = get_request_obj(request)
        barcode_ = data['barcode']
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    try:
        productObj = Temp_Product_Barcode_Scanner.objects.get(barcode=barcode_)
        product_dict = {
            'product_barcode':productObj.barcode,
            'product_title':productObj.title,
            'product_image':productObj.product_img,
            'product_category':productObj.category,
            'product_type':productObj.type
            }
        return SuccessResponse(data={'products_details':product_dict}).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=PRODUCT_NOT_FOUND).return_response_object()

#Quick Edit Shops Products
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def quick_edit_shops_product(request):
    data = get_request_obj(request)

    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    
    is_active_ = data['is_active']
    product_quantity_ = data['product_quantity']
    shop_id_ = data['shop_id']
    product_id_ = data['product_id']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']

    if Shop_Product.objects.filter(shop=shopsObject, id=product_id_):
        getProduct = Shop_Product.objects.get(id=product_id_)
        getProduct.is_active = is_active_
        getProduct.quantity = product_quantity_
        getProduct.save()
        return SuccessResponse(message=SUCCESS_UPDATED).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_PRODUCT_FOR_REQUESTED_SHOP).return_response_object()


#Add the options name for shop of variants
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def add_option_name_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    option_name_ = data['option_name']
    shop_id_ = data['shop_id']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    sellerObj = results['sellerObj']
    shopsObject = results['shopObj']

    Shop_Product_Variant_Option.objects.create(option_name=option_name_, shop=shopsObject, seller=sellerObj)
    return SuccessResponse(message=SUCCESS_CREATED).return_response_object()


#get the options name for variants of shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_option_name_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    shop_id_ = data['shop_id']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']

    getAllOptions = Shop_Product_Variant_Option.objects.filter(shop=shopsObject)
    options = []
    for obj in getAllOptions:
        option_dict_ = {
            'id':obj.id,
            'option_name':obj.option_name
            }
        options.append(option_dict_)
    return SuccessResponse(data={'options_names':options}).return_response_object()


#Delete the options name of variants of shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def delete_option_name_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    shop_id_ = data['shop_id']
    option_names_ = data['option_names']
    if request.POST:
        option_names_ = json.loads(option_names_)

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']

    for i in range(len(option_names_)):
        if Shop_Product_Variant_Option.objects.filter(shop=shopsObject, id=option_names_[i]['option_name_id']).exists():
            Shop_Product_Variant_Option.objects.get(id=option_names_[i]['option_name_id']).delete()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=OPTIONS_NOT_FOUND).return_response_object()
    return SuccessResponse(message=SUCCESS_DELETED).return_response_object()

#Update the options name of variants of shop
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def update_option_name_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    shop_id_ = data['shop_id']
    option_name_id_ = data['option_name_id']
    option_name_ = data['option_name']

    userObj = request.user

    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']
    if Shop_Product_Variant_Option.objects.filter(shop=shopsObject, id=option_name_id_).exists():
        optionObj = Shop_Product_Variant_Option.objects.get(id=option_name_id_)
        optionObj.option_name=option_name_
        optionObj.save()
        return SuccessResponse(message=SUCCESS_UPDATED).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_OPTION_FOR_REQUESTED_SHOP).return_response_object()



#Add the options value for shop of variants
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def add_option_value_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    option_value_ = data['option_value']
    option_id_ = data['option_id']

    userObj = request.user

    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj = Seller.objects.get(user=userObj)
        if Shop_Product_Variant_Option.objects.filter(id=option_id_, seller=sellerObj).exists():
            variantOptionObj = Shop_Product_Variant_Option.objects.get(id=option_id_)
            Shop_Product_Variant_Option_value.objects.create(option_value=option_value_, shop_product_variant_option=variantOptionObj)
            return SuccessResponse(message=SUCCESS_CREATED).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_OPTION_FOR_REQUESTED_SHOP).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_ACTIVE).return_response_object()


#Delete Option value of variants
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def delete_option_value_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    option_values_ = data['option_values']
    if request.POST:
        option_values_ = json.loads(option_values_)

    userObj = request.user

    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        for i in range(len(option_values_)):
            if Shop_Product_Variant_Option_value.objects.filter(id=option_values_[i]['option_value_id']).exists():
                Shop_Product_Variant_Option_value.objects.get(id=option_values_[i]['option_value_id']).delete()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message=OPTIONS_NOT_FOUND).return_response_object()
        return SuccessResponse(message=SUCCESS_DELETED).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_ACTIVE).return_response_object()




#Get the options value for shop of variants
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_option_value_for_variant(request):
    data = get_request_obj(request)
    for x in data.values():
        if x == "":
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=UNFILLED_DATA).return_response_object()
    option_id_ = data['option_id']

    userObj = request.user

    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj = Seller.objects.get(user=userObj)
        if Shop_Product_Variant_Option.objects.filter(id=option_id_, seller=sellerObj).exists():
            variantOptionObj = Shop_Product_Variant_Option.objects.get(id=option_id_)
            getAllOptions = Shop_Product_Variant_Option_value.objects.filter(shop_product_variant_option=variantOptionObj)
            options = []
            for obj in getAllOptions:
                option_dict_ = {
                    'id':obj.id,
                    'option_value':obj.option_value
                    }
                options.append(option_dict_)
            return SuccessResponse(data={'options_values':options}).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_OPTION_FOR_REQUESTED_SHOP).return_response_object()
    else:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_ACTIVE).return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def add_shop_for_seller(request):
    try:
        data = get_request_obj(request)
        role_ = data['role'].upper().strip()
        shop_name_ = data['shop_name']
        address_ = data['address']
        lat_ = data['lat']
        lng_ = data['lng']
        phone_number_ = data['phone_number']
        shop_images_ = data['shop_images']
        
        #362 24/7 Always open in whole year
        is_always_open_ = data['is_always_open']
        #open and close time for whole week
        week_times_ = data['week_times']
        if request.POST:
            week_times_ = json.loads(week_times_)
            if shop_images_ is None or shop_images_ == "":
                shop_images_ = []
            else:
                shop_images_ = json.loads(shop_images_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=PROVIDE_VALID_DATA).return_response_object()
        
    if not lat_ or not lng_ or not address_:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=UNFILLED_ADDRESS).return_response_object()

    if role_.upper().strip() != SELLER_ROLE:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()

    userObj = request.user
    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj_= Seller.objects.get(user=userObj)

        if is_always_open_ == False:
            
            week_times_check_ = validate_week_days(week_times_)
            if not week_times_check_:
                return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_SHOP_HOURS).return_response_object()


            shopObject = Shop.objects.create(lat=lat_,lng=lng_, shop_address=address_,shop_name=shop_name_ 
            ,is_always_open=is_always_open_, phone_number = phone_number_, seller=sellerObj_, week=week_times_)

            for obj in week_times_:
                shp_ = SellerShopHour.objects.create(shop=shopObject, day=obj['name'])
                sht_ = ShopHourTiming.objects.create(hour=shp_, is_open_24=obj['is_24hours'], is_close=obj['is_off'])
                if not obj['is_24hours'] and not obj['is_off']:
                    sht_.open_time = obj['open_time']
                    sht_.close_time = obj['close_time']
                    sht_.save()

        elif is_always_open_ == True:
            shopObject = Shop.objects.create(lat=lat_,lng=lng_, shop_address=address_,
            shop_name=shop_name_ ,is_always_open=is_always_open_, phone_number =phone_number_ ,seller=sellerObj_)

        for img_obj in range(len(shop_images_)):
            Shop_images.objects.create(shop=shopObject, shop_image_url=shop_images_[img_obj]['url'])
        return SuccessResponse(message=SUCCESS_CREATED).return_response_object()
    else:
        return FailureResponse(message=SELLER_NOT_FOUND,status_code=BAD_REQUEST_CODE).return_response_object()



#Delere shop of seller
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def delete_shop_of_seller(request):
    data = get_request_obj(request)

    role_ = data['role'].upper().strip()
    shop_id_ = data['shop_id']

    if role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()

    userObj = request.user
    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj_= Seller.objects.get(user=userObj)
        if Shop.objects.filter(id=shop_id_, seller=sellerObj_):
            Shop.objects.get(id=shop_id_).delete()
            return SuccessResponse(message=SUCCESS_DELETED).return_response_object()
        else:
            return FailureResponse(message=INVALID_SELLER_FOR_REQUESTED_SHOP,status_code=BAD_REQUEST_CODE).return_response_object()
    else:
        FailureResponse(status_code=BAD_REQUEST_CODE, message=SELLER_NOT_FOUND)

#Update shop of seller
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def update_shop_of_seller(request):
    data = get_request_obj(request)

    shop_id_ = data['shop_id']
    role_ = data['role'].upper().strip()
    shop_name_ = data['shop_name']
    address_ = data['address']
    lat_ = data['lat']
    lng_ = data['lng']
    phone_number_ = data['phone_number']

    #362 24/7 Always open in whole year
    is_always_open_ = data['is_always_open']
    #open and close time for whole week


    userObj = request.user
    results = validate_seller_and_shop(userObj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=results['response_message']).return_response_object()
    shopsObject = results['shopObj']

    if role_.upper().strip() != "SELLER":
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_ROLE).return_response_object()


    shopsObject.lat=lat_
    shopsObject.lng=lng_, 
    shopsObject.shop_address=address_
    shopsObject.phone_number=phone_number_
    shopsObject.shop_name=shop_name_
    shopsObject.is_always_open=is_always_open_
    shopsObject.save()
    return SuccessResponse(message=SUCCESS_UPDATED).return_response_object()


#saving propane
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def cu_propane(request):
    data = get_request_obj(request)
    print(data)
    try:
        title_ = data['title']
        desc_ = data['description']
        weight_ = data['weight']
        weight_unit_ = data['weight_unit']
        sku_ = data['sku']
        quantity_ = data['quantity']
        tags_= data['tags']
        is_active_ = data['is_active']
        category_ = data['category']
        company_id_ = data['company_id']
        role_ = data['role'].upper().strip()
        shop_id_ = data['shop_id']
        try:
            quantity_ = int(quantity_)
            company_id_ = int(company_id_)
            shop_id_ = int(shop_id_)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message=INVALID_DATA_TYPE).return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message=PROVIDE_VALID_DATA).return_response_object()
    if not type(is_active_) == bool:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                     message=INVALID_DATA_TYPE).return_response_object()
    if role_.upper().strip() != SELLER_ROLE:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message=INVALID_ROLE).return_response_object()
    if quantity_ < 1:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=INVALID_QUANTITY_AMOUNT).return_response_object()
    user_obj = request.user
    results = validate_seller_and_shop(user_obj, shop_id_)
    company_object = get_company_object(company_id_)
    if not company_object:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message=INVALID_PROPANE_COMPANY).return_response_object()
    propane_price_object = get_propane_price(company_object)
    if not propane_price_object:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message=PROPANE_PRICE_NOT_FOUND).return_response_object()
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                 message=results['response_message']).return_response_object()
    shop_object = results['shopObj']
    seller_object = results['sellerObj']
    try:
        #get propane id and update query
        propane_id_ = data['propane_id']
        if not validate_id(propane_id_):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=INVALID_DATA_TYPE).return_response_object()
        propane_id_ = int(propane_id_)
        try:
            get_propane_object = Propane.objects.get(id=propane_id_, shop=shop_object,seller=seller_object)
            if get_propane_object.sku != sku_:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=SKU_NOT_FOUND).return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="Invalid records.").return_response_object()
    except:
        if Propane.objects.filter(shop=shop_object,seller=seller_object, sku = sku_).exists():
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message=SKU_ALREADY_EXISTS).return_response_object()
        get_propane_object = Propane.objects.create(shop=shop_object,seller=seller_object, 
                                                                        company=company_object, sku=sku_)
    if not get_propane_object:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=FAILED_CREATED).return_response_object()

    get_propane_object.title = title_
    get_propane_object.description = desc_
    get_propane_object.weight = weight_
    get_propane_object.weight_unit = weight_unit_
    get_propane_object.quantity = quantity_
    get_propane_object.tags = tags_
    get_propane_object.is_active = is_active_
    get_propane_object.category = category_
    get_propane_object.price = propane_price_object.price
    get_propane_object.company=company_object
    get_propane_object.save()
    return SuccessResponse(message=SUCCESS_CREATED).return_response_object()

@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def propane_inventory(request):
    propane_array = []
    try:
        data = get_request_obj(request)
        shop_id_ = int(data['shop_id'])
        user_obj = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=PROVIDE_VALID_DATA).return_response_object()

    results = validate_seller_and_shop(user_obj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=results['response_message']).return_response_object()
    shop_object = results['shopObj']
    seller_object = results['sellerObj']
    
    try:
        propane_id_ = data['propane_id']
        try:
            propane_id_ = int(propane_id_)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=PROVIDE_VALID_DATA).return_response_object()
        try:    
            propane_object = Propane.objects.get(id=propane_id_)
            propane_dist_ = {      
                'propane_id':propane_object.id,
                'title':propane_object.title,
                'descriptin':propane_object.description,
                'weight':propane_object.weight,
                'weight_unit':propane_object.weight_unit,
                'sku':propane_object.sku,
                'quantity':propane_object.quantity,
                'tags':propane_object.tags,
                'is_active':propane_object.is_active,
                'category':propane_object.propane_category,
                'price':propane_object.price,
                'propane_company_id':propane_object.company.id,
                'propane_company_name':propane_object.company.name,
            }
            
            return SuccessResponse(data={'propane_details':propane_dist_}).return_response_object()    
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=PROPANE_NOT_FOUND).return_response_object()
    except:
        propane_objects = Propane.objects.filter(shop=shop_object)
        for object in propane_objects:
            propane_array.append({
                'id':object.id,
                'title':object.title,
                'price':object.price,
                'quantity':object.quantity,
                'is_active':object.is_active,
                'product_tag':'Propane Tank',
                'shop_id':shop_object.id,
                'seller_id':seller_object.id,
                'propane_image_url':'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/a89fadcc-431c-4327-b589-176765ba5ab2/d7pkzok-435aec37-4b26-4cd2-8a18-4b5bead57825.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2E4OWZhZGNjLTQzMWMtNDMyNy1iNTg5LTE3Njc2NWJhNWFiMlwvZDdwa3pvay00MzVhZWMzNy00YjI2LTRjZDItOGExOC00YjViZWFkNTc4MjUucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.cuQTNCeLQmtbFR4qYs05t1wpTQRtg8a_HduxIRLeuE0'
            })
        return SuccessResponse(data={'propane_inventory':propane_array}).return_response_object()
    


#Quick edit propane
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def quick_edit_and_delete_propane(request):
    try:
        data = get_request_obj(request)
        shop_id_ = data['shop_id']
        if not validate_id(shop_id_):
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_DATA_TYPE).return_response_object()

    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=PROVIDE_VALID_DATA).return_response_object()

    user_obj = request.user
    results = validate_seller_and_shop(user_obj, shop_id_)
    if results['response'] == False:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=results['response_message']).return_response_object()
    try:
        propane_delete_array = data['propane_delete_array']
        if request.POST:
            propane_delete_array = json.loads(propane_delete_array)
        for index in range(len(propane_delete_array)):
            try:
                Propane.objects.get(id=propane_delete_array[index]['propane_id']).delete()
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=FAILED_DELETED).return_response_object()
        return SuccessResponse(message=SUCCESS_DELETED).return_response_object()

    except:
        propane_id_ = data['propane_id']
        if not validate_id(propane_id_) or not validate_id(shop_id_):
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=INVALID_DATA_TYPE).return_response_object()
        quantity_ = data['propane_quantity']
        is_active_ = data['is_active']
        try:
            propane_object = Propane.objects.get(id=propane_id_)
            propane_object.quantity = int(quantity_)
            propane_object.is_active = is_active_
            propane_object.save()
            return SuccessResponse(data={'updated_quantity':quantity_},message=SUCCESS_CREATED).return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=FAILED_CREATED).return_response_object()



#Get propane companies
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=SELLER_ROLE)
def get_companies(request):
    companies = []
    try:
        propane_objects = Propane_Company.objects.all()
        for obj in propane_objects:
            companies.append({"company_id":obj.id, "company_name":obj.name})
        return SuccessResponse(data={'companies':companies}).return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=COMPANY_NOT_FOUND).return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[SELLER_ROLE])
def get_seller_order_list(request):
    try:
        data = get_request_obj(request)
        shop_id_ = int(data['shop_id'])
        # order_status = data['order_status'].strip().lower()
        # if order_status not in shop_order_list_status:
        #     return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                             message='invalid order status').return_response_object()
        user_ = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=PROVIDE_VALID_DATA).return_response_object()
    try:
        try:
            seller_ =  Seller.objects.get(user=user_)
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message=INVALID_SELLER).return_response_object()
        shop_ = Shop.objects.get(id=shop_id_, seller=seller_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=INVALID_SHOP).return_response_object()
    get_order_objects = ShopOrder.objects.filter(shop=shop_,order_status=ACCEPTED).order_by('created_at').reverse()
    order_serializer_ = GetShopOrderListSerializer(get_order_objects,many=True).data
    return SuccessResponse(data={'order_details':order_serializer_},
                                message='order information.').return_response_object()
        

#Check for orders
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True,
                          authentication_level=[SELLER_ROLE, BUYER_ROLE, DRIVER_ROLE])
def update_order_status(request):
    try:
        #need to add shop_id(later)
        data = get_request_obj(request)
        order_id_ = int(data['order_id'])
        order_status_ = data['order_status'].strip().lower()
        role_ = data['role'].strip().upper()
        if not validate_expected_role(role_):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=INVALID_ROLE).return_response_object()
        user_ = request.user
        if not order_status_ in order_status_list:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=INVALID_ORDER_STATUS).return_response_object()

        try:
            get_order = Order.objects.get(id = order_id_)
            
            #handle order status overriding
            if get_order.order_status == DISPUTED:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message=ORDER_IS_DISPUTED).return_response_object()
            
            if get_order.order_status == CANCELLED:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message=ALREADY_CANCELLED).return_response_object()
            
            if get_order.order_status == COMPLETED:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message=ALREADY_COMPLETED).return_response_object()
            
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=ORDER_NOT_FOUND).return_response_object()
        
        if role_ == BUYER_ROLE:
            if not order_status_ in buyer_order_status_list:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=INVALID_ORDER_STATUS).return_response_object()
                
            if order_status_ == CANCELLED:
                #validate if buyer is exact to the order.
                if not get_order.buyer == user_:
                        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                            message=INVALID_ORDER).return_response_object()
                
                if get_order.order_status in invalid_order_status_list_for_cancel:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message=CANCELLATION_TIME_EXPIRED).return_response_object()
                
                if Order_Items.objects.filter(order__order=get_order, item_status=DONE).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message='wait, until order is prepared.').return_response_object()
                
                try:                
                    #unable to updated the status of order to cancel when its already cancelled.
                    #get expiry from model
                    driver_accepted_time_ = get_order.driver_accepted_time
                    driver_accepted_time_ = dt.datetime.strftime(driver_accepted_time_, "%Y-%m-%d %H:%M:%S")
                    driver_accepted_time_ = utc.localize(parser.parse(driver_accepted_time_))
                    #get current time
                    time_now = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
                    time_now = utc.localize(parser.parse(time_now))
                    #get after five mints
                    driver_accepted_time_five_mints_time_expire = dt.datetime.strftime(driver_accepted_time_ + dt.timedelta(seconds=TWO_MINTS_IN_SECONDS), "%Y-%m-%d %H:%M:%S")
                    driver_accepted_time_five_mints_time_expire = utc.localize(parser.parse(driver_accepted_time_five_mints_time_expire))
                    if driver_accepted_time_ < time_now: #if accpeted time is less than now(3mints)
                        if driver_accepted_time_five_mints_time_expire < time_now: #if accpeted time is less than now(5mints)
                            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message=CANCELLATION_TIME_EXPIRED).return_response_object()
                        else:#impose panelty
                            total_amount = calculate_penalty(get_order)
                            total_amount = int(float(total_amount)*100)
                            payment_intent_object = StripeOrderPaymentIntent.objects.get(order=get_order)
                            payment_intent_id = payment_intent_object.create_payment_intent_id
                            payment_intent_capture = stripe.PaymentIntent.capture(payment_intent_id,
                                                                    amount_to_capture=total_amount)
                            payment_intent_object.capture_payment_intent_id = payment_intent_capture.id
                            update_shop_order_status(get_order, order_status_)
                            get_order.order_status = order_status_
                            get_order.save()
                            AssignOrderToDriverForAcceptence.objects.filter(order=get_order).delete()
                    else:    
                        payment_intent_object = StripeOrderPaymentIntent.objects.get(order=get_order)
                        payment_intent_id = payment_intent_object.create_payment_intent_id
                        stripe.PaymentIntent.cancel(payment_intent_id,)
                        update_shop_order_status(get_order, order_status_)
                        get_order.order_status = order_status_
                        get_order.save()
                        AssignOrderToDriverForAcceptence.objects.filter(order=get_order).delete()
                    # delete_firebase_order_node(get_order)
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=PAGE_NOT_FOUND,
                                        message=FAILED_CANCELLATION).return_response_object()
            elif order_status_ == COMPLETED:
                if not get_order.order_status == DELIVERED:
                    return FailureResponse(status_code=PAGE_NOT_FOUND,
                                        message="kindly wait, until ordered delivered.").return_response_object()
                    
                try:
                    total_amount = calculate_main_order_amount(get_order)
                    total_amount = int(float(total_amount)*100)
                    payment_intent_object = StripeOrderPaymentIntent.objects.get(order=get_order)
                    payment_intent_id = payment_intent_object.create_payment_intent_id
                    payment_intent_capture = stripe.PaymentIntent.capture(payment_intent_id,
                                                          amount_to_capture=total_amount)
                    payment_intent_object.capture_payment_intent_id = payment_intent_capture.id
                    payment_intent_object.save()
                    AssignOrderToDriverForAcceptence.objects.filter(order=get_order).delete()
                    # delete_firebase_order_node(get_order)
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=PAGE_NOT_FOUND,
                                        message=FAILED_COMPLETION).return_response_object()
                
                update_shop_order_status(get_order, order_status_)
                get_order.order_status = order_status_
                get_order.save()
            
            try:
                message_title_ = "Order "+str(order_status_)+"."
                message_body_ = "Order #"+str(get_order.id)+" is marked "+str(order_status_)+" by customer."
                notify_users_on_order_updates(get_order, message_title_, message_body_, users_roles=[DRIVER_ROLE, SELLER_ROLE])
            except Exception as e:
                print(e)
            
        elif role_ == DRIVER_ROLE:
            if not order_status_ in driver_order_status_list:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=INVALID_ORDER_STATUS).return_response_object()
            
            if order_status_ == STARTED:
                # if not get_order.order_status == PREPARED:
                if Order_Items.objects.filter(order__order=get_order, item_status=TO_DO).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message='wait, until order is prepared.').return_response_object()
                    
            if order_status_ == DELIVERED:
                if get_order.order_status == DELIVERED:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                           message=ALREADY_DELIVERED)
                try:
                    driver = Driver.objects.get(user=user_)
                    get_, created = DriverEarning.objects.get_or_create(driver=driver,order=get_order)
                    if not created:
                        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                           message=ALREADY_DELIVERED)
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                           message=SOMETHING_WENT_WRONG)
            
            update_shop_order_status(get_order, order_status_)
            get_order.order_status = order_status_
            get_order.save()
            AssignOrderToDriverForAcceptence.objects.filter(order=get_order).delete()
            #Notify buyer and seller
            try:
                message_title_ = "Order "+str(order_status_)+"."
                message_body_ = "Order #"+str(get_order.id)+" is "+str(order_status_)+" by driver."
                notify_users_on_order_updates(get_order, message_title_, message_body_, users_roles=[BUYER_ROLE, SELLER_ROLE])
            except Exception as e:
                print(e)
            
        elif role_ == SELLER_ROLE:
            if not order_status_ in shop_order_status_list:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message=INVALID_ORDER_STATUS).return_response_object()
            update_shop_order_status(get_order, order_status_)
            get_order.order_status = order_status_
            get_order.save()
            try:
                message_title_ = "Order "+str(order_status_)+"."
                message_body_ = "Order #"+str(get_order.id)+" is "+str(order_status_)+"by seller."
                notify_users_on_order_updates(get_order, message_title_, message_body_, users_roles=[DRIVER_ROLE, BUYER_ROLE])
            except Exception as e:
                print(e)
        # if not order_status_ == CANCELLED and not order_status_ == COMPLETED:
        set_firebase_order_node(get_order, order_status_)
        return SuccessResponse(message=ORDER_STATUS_UPDATED).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message=PROVIDE_VALID_DATA).return_response_object()


#Get seller completed order history  
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_seller_orders_history(request):
    try:
        user_ = request.user
        data = get_request_obj(request)
        shop_id_ = int(data['shop_id'])
        order_status = data['order_status'].lower()
        if not order_status in shop_order_list_status:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=INVALID_ORDER_STATUS).return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=INVALID_USER).return_response_object()
    try:
        shop =  Shop.objects.get(seller__user=user_, id=shop_id_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=INVALID_SHOP).return_response_object()
    try:
        if order_status == PROGRESS:
            get_order_objects = ShopOrder.objects.filter(shop=shop, order_status__in = progress_order_list).order_by('created_at').reverse()
        else:
            get_order_objects = ShopOrder.objects.filter(shop=shop, order_status = order_status).order_by('created_at').reverse()
        order_serializer_ = GetShopOrderListSerializer(get_order_objects,many=True).data
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=ORDER_NOT_FOUND).return_response_object()

#Get order item status(To do, review, done)  
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[SELLER_ROLE])
def verify_order_items_by_shoper(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        list_status = data['list_status'].lower()
        if not list_status in order_items_status:
            return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=INVALID_ORDER_STATUS).return_response_object()
        try:
            products_list = []
            shop_orders = ShopOrder.objects.filter(order__id=order_id)
            for shop_order_object in shop_orders:
                order_item_objects = Order_Items.objects.filter(order=shop_order_object, item_status=list_status)
                for order_item in order_item_objects:
                    if order_item.product is not None:
                        product_image = Shop_Product_Images.objects.filter(shop_product=order_item.product).first()
                        if product_image is not None:
                            image = product_image.image_link
                        else:
                            image = ""
                        disc = {
                            "order_id":order_id,
                            "product_id":order_item.product.id,
                            "shop_id":order_item.product.shop.id,
                            "category" : "product",
                            "title" : order_item.product.title,
                            "description":order_item.product.description,
                            "quantity" : order_item.product_quantity,
                            "price" : order_item.product.price,
                            "sale_price" : order_item.product.sale_price,
                            "image" : image
                        }
                    elif order_item.propane is not None:
                        propane_image = Propane_Images.objects.filter(propane=order_item.propane).first()
                        if propane_image is not None:
                            image = product_image.image_url
                        else:
                            image = ""
                        disc = {
                            "order_id":order_id,
                            "product_id":order_item.propane.id,
                            "shop_id":order_item.propane.shop.id,
                            "category" : "propane",
                            "title" : order_item.propane.title,
                            "description": order_item.propane.description,
                            "quantity":order_item.propane_quantity,
                            "price" : order_item.propane.price,
                            "sale_price" : 0.0,
                            "image" : image
                        }
                    products_list.append(disc)
            return SuccessResponse(data={'products':products_list},
                                    message="success.").return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=ORDER_NOT_FOUND).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=PROVIDE_VALID_DATA).return_response_object()

#verify product quantity using barcode scan
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[SELLER_ROLE])
def verify_product_using_barcode_by_shop(request):
    try:
        data = get_request_obj(request)
        shop_id = int(data['shop_id'])
        category = data['category'].upper()
        barcode = data['barcode']
        quantity = int(data['quantity'])
            
        if category == PRODUCT:
            try:
                product_object = Shop_Product.objects.get(barcode = barcode, shop__id=shop_id)
                if int(product_object.quantity) < quantity:
                    return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message='product out of stock. available quantity '+str(product_object.quantity)).return_response_object()
                else:
                    return SuccessResponse(message="success.").return_response_object()
            except Exception as e:
                print(e)
                return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message='product not found.').return_response_object()
        elif category == PROPANE:
            try:
                propane_object = Propane.objects.get(sku=barcode, shop__id=shop_id)
                if int(propane_object.quantity) < quantity:
                    return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message='product out of stock. available quantity '+str(propane_object.quantity)).return_response_object()
                else:
                    return SuccessResponse(message="success.").return_response_object()
            except Exception as e:
                print(e)
                return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message=PRODUCT_NOT_FOUND).return_response_object()
                    
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=PROVIDE_VALID_DATA).return_response_object()
            
#confirm order item quantity(increase or decrease)
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[SELLER_ROLE])
def confirm_ordered_item_quantity(request):
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        product_id = int(data['product_id'])
        category = data['category'].upper()
        quantity = int(data['quantity'])
        
        #in product case
        if category == PRODUCT:
            try:
                product_object = Shop_Product.objects.get(id=product_id)
                if int(product_object.quantity) < quantity:
                    return SuccessResponse(
                        status_code=SUCCESS_RESPONSE_CREATED,
                        data={'available_quantity':int(product_object.quantity)},
                        message="product out of stock.").return_response_object()
                else:
                    try:#order->order->id -> 'shop_order>main_order>id'
                        order_item_object = Order_Items.objects.get(order__order__id=order_id, product__id=product_id)
                        order_item_object.product_quantity = quantity
                        order_item_object.item_status = DONE
                        order_item_object.save()
                    except Exception as e:
                        print(e)
                        return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message=INVALID_ORDER_ITEM).return_response_object()
                    return SuccessResponse(message="success.").return_response_object()
            except Exception as e:
                print(e)
                return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message=PRODUCT_NOT_FOUND).return_response_object()
        #in propane case
        elif category == PROPANE:
            try:
                propane_object = Propane.objects.get(id=product_id)
                if int(propane_object.quantity) < quantity:
                    return SuccessResponse(
                        status_code=SUCCESS_RESPONSE_CREATED,
                        data={'available_quantity':int(propane_object.quantity)},
                        message="product out of stock.").return_response_object()
                else:
                    try:
                        order_item_object = Order_Items.objects.get(order__order__id=order_id, propane__id=product_id)
                        order_item_object.propane_quantity = quantity
                        order_item_object.item_status = DONE
                        order_item_object.save()
                    except Exception as e:
                        print(e)
                        return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message=INVALID_ORDER_ITEM).return_response_object()
                    return SuccessResponse(message="success.").return_response_object()
            except Exception as e:
                print(e)
                return FailureResponse(status_code=PAGE_NOT_FOUND,    
                                message=PRODUCT_NOT_FOUND).return_response_object()
                    
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message=PROVIDE_VALID_DATA).return_response_object()
    





#__________________________________________________seller acceptence________________________________
'''
#Check for orders
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=SELLER_ROLE)
def seller_orders_acceptence(request):
    try:
        data = get_request_obj(request)
        shop_order_instance_id = int(data['order_id'])
        is_accept_ = data['is_accept']
        shop_id_ =  int(data['shop_id'])
        user_ = request.user
        if not type(is_accept_)==bool:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message='please provide valid data to accept/reject order').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='please provide valid data').return_response_object()
    
    # Order.objects.filter(id=shop_order_instance_id).update(is_shop_accepted=False)
    # return HttpResponse('false')
    
    try:
        try:
            seller_ =  Seller.objects.get(user=user_)
            shop_ = Shop.objects.get(id=shop_id_, seller=seller_)
            if not ShopOrder.objects.filter(id=shop_order_instance_id, shop=shop_).exists():
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid order').return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='invalid seller').return_response_object()
        
        if is_accept_:
            try:
                get_shop_order_object_ = ShopOrder.objects.get(id=shop_order_instance_id)
                get_shop_order_object_.order_status = ACCEPTED
                get_shop_order_object_.is_shop_accepted=is_accept_
                get_shop_order_object_.save()
                order_object_ = get_shop_order_object_.order
            except Exception as e:
                print(e)
            #notify buyer
            try:
                buyer_ = order_object_.buyer
                message_title_ = "Order accepted by "+str(shop_.shop_name)+" shop."
                message_body_ = "Your order has been accepted by shop."
                notify_user(buyer_, message_title_, message_body_)
            except:
                pass
            #check if all shops accepted buyer's order.
            #details: if buyer orders from different shops, the 'is_order_ready_flag' will become True when all all shop accept orders.
            try:
                is_order_ready_flag_ = True
                get_all_buyer_order_objects_ = ShopOrder.objects.filter(order=order_object_)
                for buyer_order_object in get_all_buyer_order_objects_:
                    if buyer_order_object.is_shop_accepted == False:
                        is_order_ready_flag_ = False
                
                #if all orders accepted by shops than assign order to multiple drivers for acceptence
                if is_order_ready_flag_:
                    order_object_.is_shops_accepted = True
                    
                    get_all_active_drivers_objects_ = Driver.objects.filter(is_active = True)
                    buyer_lat_ = get_shop_order_object_.order.shipping_address.lat
                    buyer_lng_ = get_shop_order_object_.order.shipping_address.lng
                    for active_driver_object in get_all_active_drivers_objects_:
                        try:
                            is_assignable_order_to_driver_ = get_driver_objects_within_distance(active_driver_object,
                                                                                        buyer_lat_ ,buyer_lng_)
                        except Exception as e:
                            print(Fore.YELLOW, e, 'unable to assign some driver')
                        #Assign orders to driver for acceptence
                        if is_assignable_order_to_driver_:
                            assigned_object = AssignOrderToDriverForAcceptence.objects.create(driver=active_driver_object,
                                                                                              order=order_object_)
                            for buyer_order_object in get_all_buyer_order_objects_:
                                AssignOrderListToDriver.objects.create(assign_order=assigned_object,order=buyer_order_object)
            except:
                pass
            set_firebase_order_node(order_object_)
            return SuccessResponse(message='order accepted.').return_response_object()
        else:
            ShopOrder.objects.filter(id=shop_order_instance_id).delete()
            return SuccessResponse(message='order rejected.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='unable to update order status, try again').return_response_object()

'''


# @decorator_.rest_api_call(allowed_method_list=['POST'])
# def upload_img(request):
#     img = request.FILES["product_img"]
#     ext = img.name.split('.')[-1]
#     name = img.name.split('.')[0].replace(" ", "")
#     imgUrl = Amazon().upload_to_aws(name,img, ext)
#     return SuccessResponse(data={'Image url':imgUrl}).return_response_object()