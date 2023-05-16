from utilities.models import kwkChargesStructure
from seller.reuselable_resources import get_shop_rates
from buyer.serializer import GetOrderDetailsSerializer, GetOrderTrackingSerialzer
import json
from re import T
import requests
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from utilities.reuseableResources import *
from authModule.models import *
from django.http import QueryDict
from seller.models import *
import kwk.settings
import datetime
from pyfcm import FCMNotification
from geopy.distance import geodesic
import re
from uuid import uuid4
import numpy as np
from datetime import date
from datetime import datetime
from django.db.models import Avg
from kwk.settings import *


#get data from request
def get_request_obj(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        try:
            data = json.loads(request.body.decode())
        except:
            data = request.POST
    return data

#validate null values in request
def validate_null_values(data):
    for x in data.values():
        if x == "":
            return False
    return True

#validate input role in expected roles
def validate_expected_role(role_):
    if (not role_ == BUYER_ROLE) and (not role_ == DRIVER_ROLE) and (not role_ == SELLER_ROLE):
        return False
    return True

#validate email format
def validate_email_format(email):
    if not (re.search(regex, email)):
        return False
    return True

#get email first part abc@email.com as 'abc'
def get_email_first_part(email):
    try:
        first_part = email.split("@")[0]
        return first_part
    except Exception as e:
        print(e)

#validate password
def validate_password(password):
    if len(password)<8 or len(password)>20:
        return False
    return True

#validate social security number(SSN)
def validate_ssn(ssn):
    if not (re.search(snn_regex, ssn)):
        return False
    return True

#validate drive age
def validate_driver_age(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if not age >= 21:
        return False
    return True

#checkr required basic data
def checkr_basic_data_null_validation(first_name, last_name, email, dob, phone, ssn, zip):
    if not first_name or not last_name or not email or not dob or not phone or not ssn or not zip:
        return False
    return True

#validate driver related info
def validate_driver_info(auto_insurance_number_, vehicle_number_, license_number_):
    if not auto_insurance_number_ or not vehicle_number_ or not license_number_:
        return False
    return True

#concatinate strings
def concat_errors_string(old_str, new_str):
    concat_string = old_str+'@'+new_str
    return concat_string

#generate randome token for email verification
def generate_email_verification_token():
    verification_token = str(uuid4())
    return verification_token

#generate randome otp number
def generate_six_digits_code():
    random_code = ''.join(map(str,np.random.randint(1,9,3))) + ''.join(map(str,np.random.randint(1,9,3)))
    return random_code
    
#html contents to send otp on email
def get_html_for_otp(otp):
    html_content = "<!DOCTYPE html> <html> <head> <title></title> <meta http-equiv='Content-Type' content='text/html; charset=utf-8' /> <meta name='viewport' content='width=device-width, initial-scale=1'> <meta http-equiv='X-UA-Compatible' content='IE=edge' /> <style type='text/css'> @media screen { @font-face { font-family: 'Lato'; font-style: normal; font-weight: 400; src: local('Lato Regular'), local('Lato-Regular'), url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: normal; font-weight: 700; src: local('Lato Bold'), local('Lato-Bold'), url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: italic; font-weight: 400; src: local('Lato Italic'), local('Lato-Italic'), url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: italic; font-weight: 700; src: local('Lato Bold Italic'), local('Lato-BoldItalic'), url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format('woff'); } } /* CLIENT-SPECIFIC STYLES */ body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; } table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; } img { -ms-interpolation-mode: bicubic; } /* RESET STYLES */ img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; } table { border-collapse: collapse !important; } body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; } /* iOS BLUE LINKS */ a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; } /* MOBILE STYLES */ @media screen and (max-width:600px) { h1 { font-size: 32px !important; line-height: 32px !important; } } /* ANDROID CENTER FIX */ div[style*='margin: 16px 0;'] { margin: 0 !important; } </style> </head> <body style='background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;'> <!-- HIDDEN PREHEADER TEXT --> <div style='display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;'> We're thrilled to have you here! Get ready to dive into your new account. </div> <table border='0' padding='50px' cellpadding='0' cellspacing='0' width='100%'> <!-- LOGO --> <tr> <td bgcolor='#FFA73B' align='center'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td align='center' valign='top' style='padding: 40px 10px 40px 10px;'> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#FFA73B' align='center'' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#ffffff' align='center' valign='top' style='padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;'> <h1 style='font-size: 48px; font-weight: 400; margin: 2;'>Welcome!</h1> <img src='https://img.icons8.com/clouds/100/000000/handshake.png' width='125' height='120' style='display: block; border: 0px;' /> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#ffffff' align='left' style='padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='margin: 0; padding:20px;'>We're excited to have you get started. First, you need to confirm your account. Type the below code in kwkApp.</p> </td> </tr> <tr> <td bgcolor='#ffffff' align='left'> <table width='100%' border='0' cellspacing='0' cellpadding='0'> <tr> <td bgcolor='#ffffff' align='center' style='padding: 20px 30px 60px 30px;'> <table border='0' cellspacing='0' cellpadding='0'> <tr> <td align='center' style='border-radius: 3px;' bgcolor='#FFA73B'><span style='font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #FFA73B; display: inline-block;'>" + otp + "</span></td> </tr> </table> </td> </tr> </table> </td> </tr> <!-- COPY --> <tr> <td bgcolor='#ffffff' align='left' style='padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='padding: 20px;'>If you have any questions, just reply to this email—we're always happy to help out.</p> </td> </tr> <tr> <td bgcolor='#ffffff' align='left' style='padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='padding: 20px;'>Cheers,<br>kwk-drop Team</p> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 30px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#FFECD1' align='center' style='padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <h2 style='font-size: 20px; font-weight: 400; color: #111111; margin: 0;'>Need more help?</h2> <p style='margin: 0;'><a href='#' target='_blank' style='color: #FFA73B;'>We&rsquo;re here to help you out</a></p> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#f4f4f4' align='left' style='padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;'> <br> <p style='margin: 0;'>If these emails get annoying, please feel free to <a href='#' target='_blank' style='color: #111111; font-weight: 700;'>unsubscribe</a>.</p> </td> </tr> </table> </td> </tr> </table> </body> </html>"
    return html_content

#html contents to send verification link on email
def get_html_for_email_verification(link,token):
    html_content = "<!DOCTYPE html> <html> <head> <title></title> <meta http-equiv='Content-Type' content='text/html; charset=utf-8' /> <meta name='viewport' content='width=device-width, initial-scale=1'> <meta http-equiv='X-UA-Compatible' content='IE=edge' /> <style type='text/css'> @media screen { @font-face { font-family: 'Lato'; font-style: normal; font-weight: 400; src: local('Lato Regular'), local('Lato-Regular'), url(https://fonts.gstatic.com/s/lato/v11/qIIYRU-oROkIk8vfvxw6QvesZW2xOQ-xsNqO47m55DA.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: normal; font-weight: 700; src: local('Lato Bold'), local('Lato-Bold'), url(https://fonts.gstatic.com/s/lato/v11/qdgUG4U09HnJwhYI-uK18wLUuEpTyoUstqEm5AMlJo4.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: italic; font-weight: 400; src: local('Lato Italic'), local('Lato-Italic'), url(https://fonts.gstatic.com/s/lato/v11/RYyZNoeFgb0l7W3Vu1aSWOvvDin1pK8aKteLpeZ5c0A.woff) format('woff'); } @font-face { font-family: 'Lato'; font-style: italic; font-weight: 700; src: local('Lato Bold Italic'), local('Lato-BoldItalic'), url(https://fonts.gstatic.com/s/lato/v11/HkF_qI1x_noxlxhrhMQYELO3LdcAZYWl9Si6vvxL-qU.woff) format('woff'); } } /* CLIENT-SPECIFIC STYLES */ body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; } table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; } img { -ms-interpolation-mode: bicubic; } /* RESET STYLES */ img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; } table { border-collapse: collapse !important; } body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; } /* iOS BLUE LINKS */ a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; } /* MOBILE STYLES */ @media screen and (max-width:600px) { h1 { font-size: 32px !important; line-height: 32px !important; } } /* ANDROID CENTER FIX */ div[style*='margin: 16px 0;'] { margin: 0 !important; } </style> </head> <body style='background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;'> <!-- HIDDEN PREHEADER TEXT --> <div style='display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;'> We're thrilled to have you here! Get ready to dive into your new account. </div> <table border='0' padding='50px' cellpadding='0' cellspacing='0' width='100%'> <!-- LOGO --> <tr> <td bgcolor='#FFA73B' align='center'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td align='center' valign='top' style='padding: 40px 10px 40px 10px;'> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#FFA73B' align='center'' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#ffffff' align='center' valign='top' style='padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;'> <h1 style='font-size: 48px; font-weight: 400; margin: 2;'>Welcome!</h1> <img src='https://img.icons8.com/clouds/100/000000/handshake.png' width='125' height='120' style='display: block; border: 0px;' /> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#ffffff' align='left' style='padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='margin: 0; padding:20px;'>We're excited to have you get started. First, you need to confirm your account. Type the below code in kwkApp.</p> </td> </tr> <tr> <td bgcolor='#ffffff' align='left'> <table width='100%' border='0' cellspacing='0' cellpadding='0'> <tr> <td bgcolor='#ffffff' align='center' style='padding: 20px 30px 60px 30px;'> <table border='0' cellspacing='0' cellpadding='0'> <tr> <td align='center' style='border-radius: 3px;' bgcolor='#FFA73B'><a href='"+str(link)+"?token="+str(token)+"'><span style='font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #FFA73B; display: inline-block;'>Verify</span></a></td> </tr> </table> </td> </tr> </table> </td> </tr> <!-- COPY --> <tr> <td bgcolor='#ffffff' align='left' style='padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='padding: 20px;'>If you have any questions, just reply to this email—we're always happy to help out.</p> </td> </tr> <tr> <td bgcolor='#ffffff' align='left' style='padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <p style='padding: 20px;'>Cheers,<br>kwk-drop Team</p> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 30px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#FFECD1' align='center' style='padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;'> <h2 style='font-size: 20px; font-weight: 400; color: #111111; margin: 0;'>Need more help?</h2> <p style='margin: 0;'><a href='#' target='_blank' style='color: #FFA73B;'>We&rsquo;re here to help you out</a></p> </td> </tr> </table> </td> </tr> <tr> <td bgcolor='#f4f4f4' align='center' style='padding: 0px 10px 0px 10px;'> <table border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width: 600px;'> <tr> <td bgcolor='#f4f4f4' align='left' style='padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;'> <br> <p style='margin: 0;'>If these emails get annoying, please feel free to <a href='#' target='_blank' style='color: #111111; font-weight: 700;'>unsubscribe</a>.</p> </td> </tr> </table> </td> </tr> </table> </body> </html>"
    return html_content
    

#Validate is seller role and shop relation with seller
def validate_seller_and_shop(userObj, shop_id_=0):
    if UserProfile.objects.filter(is_seller=True, user=userObj).exists():
        sellerObj = Seller.objects.get(user=userObj)
        if Shop.objects.filter(id=shop_id_, seller=sellerObj).exists():
            shopsObject = Shop.objects.get(id=shop_id_)
            return ({'sellerObj':sellerObj, 'shopObj':shopsObject, 'response':True})
        else:
            return ({'response_message':'Shop does not belong to the requested seller', 'response':False})
    else:
        return ({'response_message':'Seller role is not active', 'response':False})


#Validate is seller role and shop relation with seller
def validate_buyer(userObj):
    if UserProfile.objects.filter(is_buyer=True, user=userObj).exists():
        buyerObj = UserProfile.objects.get(user=userObj)
        return ({'buyerObj':buyerObj, 'response':True})
    else:
        return ({'response_message':'Buyer role is not active', 'response':False})

#Validate Driver
def validate_driver(userObj):
    if UserProfile.objects.filter(is_driver=True, user=userObj).exists():
        driverObj = Driver.objects.get(user=userObj)
        return ({'driverObj':driverObj, 'response':True})
    else:
        return ({'response_message':'Driver role is not active', 'response':False})


#Shops Controller
def get_shops_objects(getAllShops):
    shopsArray = []
    for shopObj in getAllShops:

        shopImage = Shop_images.objects.filter(shop=shopObj).last()
        if shopImage is not None:
            shopImageUrl = shopImage.shop_image_url
        else:
            shopImageUrl = ""
        shop_disc = {
                    'shop_id':shopObj.id,
                    'shop_name':shopObj.shop_name,
                    'shop_image_url':shopImageUrl,
                    'shop_total_rates':10,
                    'eta':'ETA: 10 mints',
                    }
        shopsArray.append(shop_disc)
    return shopsArray


#Shops Controller
def get_shops_objects_within_distance(getAllShops,buyer_lat,buyer_lon):
    shopsArray = []
    for shopObj in getAllShops:
        distance=get_distance_buyer_seller(buyer_lat,buyer_lon,shopObj.lat,shopObj.lng)
        if distance>5:
            continue
        eta_time=get_ETA_buyer_seller(buyer_lat,buyer_lon,shopObj.lat,shopObj.lng)
        if eta_time< 30:
            eta_time=30
        shopImage = Shop_images.objects.filter(shop=shopObj).last()
        if shopImage is not None:
            shopImageUrl = shopImage.shop_image_url
        else:
            shopImageUrl = ""
        get_rates = get_shop_rates(shopObj)
        shop_disc = {
                    'shop_id':shopObj.id,
                    'shop_name':shopObj.shop_name,
                    'shop_image_url':shopImageUrl,
                    'shop_total_rates':get_rates,
                    'eta':'ETA:'+ str(int(eta_time)) + ' mints',
                    }
        print(shopObj,'end')
        shopsArray.append(shop_disc)
    return shopsArray

#Get driver objects within buyer distance
def get_driver_objects_within_distance(driver_,buyer_lat,buyer_lon):
    driver_radius_obj = DriverRadiusSettings.objects.get(driver=driver_)
    distance=get_distance_buyer_driver(buyer_lat,buyer_lon,driver_radius_obj.lat,driver_radius_obj.lng)
    # if distance > driver_radius_obj.radius:
    #     return False
    
    return True


#Products Controller
def get_products_objects(get_products):
    product_list = []
    for product in get_products:
        product_disc = get_product(product)
        product_list.append(product_disc)
    return product_list

#get single product object
def get_product(product_object):
    if Shop_Product_Images.objects.filter(shop_product=product_object).exists():
            productImagesObj = Shop_Product_Images.objects.filter(shop_product=product_object).first()
            productImgLink = productImagesObj.image_link
    else:
        productImgLink = ""
    try:
        product_rates = ProductReview.objects.filter(product=product_object).aggregate(rates = Avg('review_in_star'))
        product_rates = round(float(product_rates['rates']), 1)

    except Exception as e:
        product_rates = 5.0
        print(e)
    
    product_disc = {
        'category':'product',
        'product_id':product_object.id,
        'shop_id':product_object.shop.id,
        'shop_name':product_object.shop.shop_name,
        'seller_id' : product_object.seller.id,
        'vendor_id' : product_object.vendor.id,
        'product_title':product_object.title,
        'product_description':product_object.description,
        'is_active': product_object.is_active,
        'sku' : product_object.sku,
        'barcode' : product_object.barcode,
        'quantity' : product_object.quantity,
        'cart_quantity' : 0,
        'tags': product_object.tags,
        'company_id' : -1,
        'company_name' : '',
        'product_price':product_object.price,
        'product_sale_price':product_object.sale_price,
        'product_weight':product_object.weight,
        'product_weight_unit':product_object.weight_unit,
        'product_image_url':productImgLink,
        'product_total_rates':product_rates,
        'eta':'ETA: 10 mints',
        }
    return product_disc

#SHOP_ETA
def get_ETA_buyer_seller(buyer_lat,buyer_lng,seller_lat,seller_lng):
    try:
        distance_km=geodesic((float(seller_lat),float(seller_lng)),(buyer_lat,buyer_lng)).km
        print(distance_km)
        eta = (distance_km/40) * 60  # e.g. 'km/speed of car)*seconds'
        if eta < 1:
            eta = 1
        return eta

    except Exception as e:
        print(e)

#get buyer distance
def get_distance_buyer_seller(buyer_lat,buyer_lon,seller_lat,seller_lng):
    try:
        distance_km=geodesic((float(seller_lat),float(seller_lng)),(float(buyer_lat),float(buyer_lon))).km
        distance_km = round(distance_km, 2)
        return distance_km
    except Exception as e:
        print(e)
        
#Driver ETA
def get_ETA_buyer_driver(buyer_lat,buyer_lng,driver_lat,driver_lng):
    try:
        distance_km=geodesic((float(driver_lat),float(driver_lng)),(buyer_lat,buyer_lng)).km
        eta = (distance_km/40) * 60  # e.g. 5km / 40(car speed)
        if eta < 1:
            eta = 1
        return eta
    except Exception as e:
        print(e)

#get driver distance
def get_distance_buyer_driver(buyer_lat,buyer_lon,driver_lat,driver_lng):
    try:
        distance_km=geodesic((float(driver_lat),float(driver_lng)),(float(buyer_lat),float(buyer_lon))).km
        return distance_km
    except Exception as e:
        print(e)
 
def get_propane_object(get_propane):
    propane_disc = {
        'category':'propane',
        'product_id':get_propane.id,
        'shop_id':get_propane.shop.id,
        'shop_name':get_propane.shop.shop_name,
        'vendor_id' : 0,
        'product_title':get_propane.title,
        'seller_id' : get_propane.seller.id,
        'product_description' : get_propane.description,
        'is_active' : get_propane.is_active,
        'sku' : get_propane.sku,
        'barcode' : '',
        'quantity' : get_propane.quantity,
        'cart_quantity' : 0,
        'propane_category' : get_propane.propane_category,
        'tags' : get_propane.tags,
        'company_id' : get_propane.company.id,
        'company_name' : get_propane.company.name,
        'product_price':get_propane.price,
        'product_sale_price':0.0,
        'product_weight':get_propane.weight,
        'product_weight_unit':get_propane.weight_unit,
        'product_image_url':"https://5.imimg.com/data5/ES/DF/IY/SELLER-19039039/propane-gases-250x250.jpg",
        'product_total_rates':10,
        'eta':'ETA: 10 mints'
        }
    return propane_disc
 
#Propanes Controller
def get_propane_objects(get_propanes):
    propane_list = []    
    for propane_object in get_propanes:
        product_disc = get_propane_object(propane_object)
        propane_list.append(product_disc)
    return propane_list

#Propanes Controller ETA base
def get_propane_objects_within_distance(get_all_propanes,lat,lng):
    propane_list = []
    for propane_object in get_all_propanes:
        distance=get_distance_buyer_seller(lat,lng,propane_object.shop.lat,propane_object.shop.lng)
        if distance >5:
            continue
        eta_time=get_ETA_buyer_seller(lat,lng,propane_object.shop.lat,propane_object.shop.lng)
        # if eta_time< 30:
        #     eta_time=30
        propane_disc = get_propane_object(propane_object)
        propane_disc.update({'eta':'ETA: '+ str(int(eta_time)) + ' mints'})
        propane_list.append(propane_disc)
    return propane_list

#Propanes Controller
def get_product_objects_within_distance(products,lat,lng):
    propane_list = []
    for product in products:
        distance=get_distance_buyer_seller(lat,lng,product.shop.lat,product.shop.lng)
        if distance >5:
            continue
        eta_time=get_ETA_buyer_seller(lat,lng,product.shop.lat,product.shop.lng)
        # if eta_time< 30:
        #     eta_time=30
        product_disc = get_product(product)
        product_disc.update({'eta':'ETA: '+ str(int(eta_time)) + ' mints'})
        propane_list.append(product_disc)
    return propane_list

#Propane_for_suggest_list
def get_propane_object_details_for_suggesionlist(propane, category):
    dest = {
            "propane_category_type":category,
            "propane_price": propane.price,
            "propane_eta":"30 Mins",
            "propane_id": int(propane.id),
            "shop_id":int(propane.shop.id),
            "shop_name": propane.shop.shop_name,
            "image" : "https://5.imimg.com/data5/ES/DF/IY/SELLER-19039039/propane-gases-250x250.jpg"
        }
    return dest
    

#-->Checkr
def create_candidate(candidate_data):
    response = requests.post('https://api.checkr.com/v1/candidates', data=candidate_data,
                             auth=(kwk.settings.CHECKER_TEST_API_SECRET_KEY, ''))
    if response.status_code == 200 or response.status_code == 201:
        return response, True
    return response, False

def create_report(report_data):
    response = requests.post('https://api.checkr.com/v1/reports', data=report_data, auth=(kwk.settings.CHECKER_TEST_API_KEY, ''))
    if response.status_code == 200 or response.status_code == 201:
        return response, True
    return response, False

def check_report_status(report_id):
    response = requests.get('https://api.checkr.com/v1/reports/'+report_id, auth=(kwk.settings.CHECKER_TEST_API_KEY, ''))
    return response.json()['status']
#<--Checkr


#shop timing pasrser
def get_parse_time(time):
    try:
        date_time_ = datetime.datetime.strptime(time, '%H:%M')
        return date_time_.time()
    except:
        return False

#valiate null addresses
def validate_null_address(lat, lng, address):
    if not lat or not lng or not address:
        return False
    return True

#shop timing validator
def validate_week_days(week_days):
    is_valid_value = True
    response_days = []

    for obj in week_days:
        if obj['name'] not in WEEK_DAYS_NAME:
            is_valid_value = False
        else:
            response_days.append(obj['name'])

        if not obj['is_24hours'] and not obj['is_off']:
            open_time = datetime.strptime(obj['open_time'], "%H:%M").strftime("%H:%M")
            close_time = datetime.strptime(obj['close_time'], "%H:%M").strftime("%H:%M")
            if open_time and close_time:
                if open_time > close_time:
                    is_valid_value = False
            else:
                is_valid_value = False

    response_days = set(response_days)
    if len(response_days) != 7:
        is_valid_value = False
    return is_valid_value



#FCM
def send_push(message_title, message_body, registration_ids, extra_notification_kwargs=None):
    push_service = FCMNotification(api_key=kwk.settings.FCM_API_KEY)
    respons = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                         message_body=message_body, message_title=message_title,
                                         extra_notification_kwargs=extra_notification_kwargs,
                                         sound=NOTIFICATION_SOUND)
    return respons

#get company list
def get_company_object(company_id):
    try:
        company_object_ = Propane_Company.objects.get(id=company_id)
        return company_object_
    except:
        return False;

#get company price
def get_propane_price(propane_company_object):
    try:
        propane_price_object_ = Propane_Price.objects.get(propane_company=propane_company_object)
        return propane_price_object_
    except:
        return False;

#validate id
def validate_id(value):
    try:
        value = int(value)
        return True
    except:
        return False

#Notify single
def notify_user(user, message_title, message_text):
    fcm_object_ = FCMDevices.objects.get(user=user)
    fcm_list = []
    fcm_token_ = fcm_object_.fcm_token
    fcm_list.append(fcm_token_)
    message_title_ = message_title
    message_body_ = message_text
    send_push(message_title_, message_body_, fcm_list)
    
    #Notify multiple users
def notify_multiple_users(users, message_title, message_text):
    fcm_object_ = FCMDevices.objects.filter(user__in=users).values_list('fcm_token',flat=True)
    fcm_object_ = list(fcm_object_)
    message_title_ = message_title
    message_body_ = message_text
    send_push(message_title_, message_body_, fcm_object_)
    
#create or update order node on Firabase
def set_firebase_order_node(order, status):
    order_serialized_object = GetOrderDetailsSerializer(order).data
    data = {
        "order_status":status
    }
    FIREBASE_DATABASE.child("orders").child(order.id).set(data)
    
#set order tracking info on firebase
def set_firebase_order_tracking_info(order):
    addresses = GetOrderTrackingSerialzer(order).data
    FIREBASE_DATABASE.child("order_tracking").child(order.id).set(addresses)
    
#delete firebase order node
def delete_firebase_order_node(order):
    FIREBASE_DATABASE.child("orders").child(order.id).remove()
    
def get_delivery_and_service_charges(shops, buyer):
    delivery_fee = 0.0
    service_fee = 0.0
    total_km = 0
    get_charges = kwkChargesStructure.objects.filter(service_charges_in_percentage__gt=0,
                                                            delivery_charges_per_kilometer__gt=0
                                                            ).last()
    for shop_id in shops:
        shop_object = Shop.objects.get(id=int(shop_id['shop_id']))
        shop_lat = shop_object.lat
        shop_lng = shop_object.lng
        buyer_address_object =  User_Addresses.objects.filter(user=buyer, is_default=True).last()
        km = get_distance_buyer_seller(buyer_address_object.lat,buyer_address_object.lng,shop_lat,shop_lng)
        total_km = total_km+km
    delivery_fee = float(get_charges.delivery_charges_per_kilometer*total_km)
    delivery_fee = round(delivery_fee, 2)
    if delivery_fee < 5:
        delivery_fee = 5.0
    service_fee = get_charges.service_charges_in_percentage
    return delivery_fee, service_fee