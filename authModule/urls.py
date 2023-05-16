from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *
from .driver import register_driver
from .seller import register_seller

    # path('login-with-phone/',login_with_phone),
    # path('validate-otp-and-login/',validate_otp_and_login),


urlpatterns = [
    # path('register/', register),
    path('login/', login),
    path('login-with-phonenumber/',login_with_phonenumber),
    # path('send-otp-on-phonenumber-to-login/',send_otp_on_phonenumber_to_login),
    # path('validate-phonenumber-otp-and-login-directly/',validate_phonenumber_otp_and_login_directly),
    path('logout/', logout),
    #register buyer
    path('register-buyer/', register_buyer),
    path('email-verification/',email_verification),
    path('add-phonenumber/', add_phonenumber),
    #Reset password
    path('send-and-resend-email-otp-to-reset-password/',send_and_resend_email_otp_to_reset_password),#send otp to reset password(email)
    path('validate-reset-password-otp/', validate_reset_password_otp), #validate reset password otp(email)
    path('create-new-password/', create_new_password,),
    # path('check-driver-record/', check_driver_record), #remove later
    # path('check-seller-record/', check_seller_record), #remove later
    path('register-driver/', register_driver),
    path('register-seller/', register_seller),
    path('create-bank-account-verification/', create_bank_accont_verification),
    path('switch-role/', switch_role),
    #phone number otp(not yet done)
    # path('send-otp-on-phonenumber/', send_otp_on_phonenumber),
    # path('validate-phone-number-otp/', validate_phone_number_otp),
    
    path('create-fcm-device/', create_fcm_device),
    #utilies
    path('check-user-previews-password/',check_user_previews_password),#check user password of active roles when create new role.
        
#only testing(later remove)
    path('notify-user-testing/', notify_user_testing),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
