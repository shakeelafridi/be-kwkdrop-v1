from datetime import datetime, timedelta
from twilio.rest.api.v2010.account import message
from colorama.ansi import Fore
from requests.sessions import HTTPAdapter
from authModule.models import License, FCMDevices, Driver, ResetPassword, PhoneNumbers
from utilities.reuseableResources import *
from utilities.RequestHandler import *
from utilities.ResponseHandler import *

import pytz
utc = pytz.UTC
import datetime as dt

from dateutil import parser
decorator_ = DecoratorHandler()
jwt_ = JWTClass()

#Expire email otp after each 1 mins
def email_otp_code_expiry():
    timeNow = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
    ResetPassword.objects.filter(key_expires__lte = utc.localize(parser.parse(timeNow))).delete()

#Expire phone number otp after each 1 mins
def phone_number_otp_code_expiry():
    timeNow = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
    PhoneNumbers.objects.filter(key_expires__lte = utc.localize(parser.parse(timeNow))).delete()

def notified_on_expire_license(request):
    threshold = datetime.today() - timedelta(days=30)
    reg_id = License.objects.filter(license_exp_date__gte=threshold,
                                    license_exp_date__lte=datetime.today().date()
                                    ).values_list('driver__user', flat=True)
    fcm_token = FCMDevices.objects.filter(user__in=reg_id).values_list('fcm_token', flat=True)
    message_title = 'License Expiry'
    message_body = 'Your license is about to expire.'
    send_push(message_title, message_body, list(fcm_token))
    

def notified_on_expire_insurance(request):
    threshold = datetime.today() - timedelta(days=30)
    reg_id = Driver.objects.filter(auto_insurance_expiry__gte=threshold,
                                   auto_insurance_expiry__lte=datetime.today().date()
                                   ).values_list('user', flat=True)
    fcm_token = FCMDevices.objects.filter(user__in=reg_id).values_list('fcm_token', flat=True)
    message_title = 'Auto insurance Expired'
    message_body = 'Your auto insurance is about to expire.'
    msg = send_push(message_title, message_body, list(fcm_token))
    
#keep find driver for order after every 1 mints, to those orders which driver is not assinged.
def find_driver_nearby_buyer_for_order(request):
    try:
        order_objects = Order.objects.filter(is_drivers_accepted=False)
        for order_object in order_objects:
            get_all_buyer_order_objects_ = ShopOrder.objects.filter(order=order_object)
            try:
                get_all_active_drivers_objects_ = Driver.objects.filter(is_active = True)
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


    # fcm_token = "eBH_JcMNRU-juRcz5DUNTt:APA91bGYM_kq0i2BVfBl06xNraZMTlkYGQQStxkmU-Kfih7WA0K8faxfDpdXEj-qYV75t5Fl4ZCTFWEeNum_d8NJoK9xSXPy-7v0FtW0IictDLUtmR2ENQSE0SF226vgFeqAllrogW-g"
    # message_title = 'Test'
    # message_body = 'This is testing notifications.'
    # print(list(fcm_token))
    # fcm_list = []
    # fcm_list.append(fcm_token)
    # # msg = send_push(message_title, message_body, list(fcm_token))
    # msg = send_push(message_title, message_body, fcm_list)
    # return SuccessResponse(message=msg).return_response_object()