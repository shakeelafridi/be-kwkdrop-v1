# from django.shortcuts import render
# from pyfcm import FCMNotification
# from authModule.models import User, FCMDevices
# from utilities.RequestHandler import *
# from utilities.ResponseHandler import *
# from utilities.reuseableResources import *
# from kwk.settings import *

# @decorator_.rest_api_call(allowed_method_list=['POST'] ,is_authenticated=True, 
#                             authentication_level=[DRIVER_ROLE, BUYER_ROLE, SELLER_ROLE])
# def send_push(message_title, message_body, registration_ids, extra_notification_kwargs=None):
#     push_service = FCMNotification(api_key=settings.FCM_API_KEY)
#     push_service.notify_multiple_devices(registration_ids=registration_ids,
#                                          message_body=message_body, message_title=message_title,
#                                          extra_notification_kwargs=extra_notification_kwargs)


# @decorator_.rest_api_call(allowed_method_list=['GET'] ,is_authenticated=True, 
#                             authentication_level=[DRIVER_ROLE, BUYER_ROLE, SELLER_ROLE])
# def send(request):
#     data = request
#     fcm_token = FCMDevices.objects.filter(user__in=data.get('user')).values_list('fcm_token', flat=True)
#     extra_notification_kwargs = {
#         'image': data.get('image.url')
#     }
#     send_push(data.get('title'), data.get('body'), list(fcm_token), extra_notification_kwargs)
