from django.shortcuts import redirect
from utilities.RequestHandler import *
from utilities.ResponseHandler import *
from utilities.reuseableResources import *
from utilities.response_messages import *
from kwk.settings import *
from .models import *
from django.contrib.auth import authenticate
from utilities.jwt import JWTClass
import datetime as dt
from dateutil import parser
import pytz
utc = pytz.UTC
from django.core.mail import EmailMultiAlternatives
decorator_ = DecoratorHandler()
jwt_ = JWTClass()
import stripe
stripe.api_key = STRIP_SECRET_KEY
# from twilio.rest import Client

#login
@decorator_.rest_api_call(allowed_method_list=['POST'])
def login(request):
    data = get_request_obj(request)
    try:
        email_ = data['email'].lower().strip()
        password_ = data['password']
        role_ = data['role'].upper().strip()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message="please provide valid data.").return_response_object()
    
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message="please fill all the fields.").return_response_object()

    if not Role.objects.filter(name=role_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    try:
        user_obj = User.objects.get(username=email_)
        user_profile = UserProfile.objects.get(user=user_obj)
    except:
        return FailureResponse(status_code=PAGE_NOT_FOUND, message='email does not exists.').return_response_object()


    # Check login for Seller
    if role_.upper().strip() == SELLER_ROLE:
        if user_profile.is_seller and Seller.objects.filter(user=user_obj).exists():
            user = authenticate(username=email_, password=password_)
            if user:
                user.userprofile.is_active = True
                user.userprofile.save()
                token = jwt_.create_user_session(user)
                return SuccessResponse(data={'token': token}).return_response_object()

            else:
                return FailureResponse(message='Invalid password',
                                       status_code=BAD_REQUEST_CODE).return_response_object()
        else:
            return FailureResponse(message='Seller Role is not active',
                                   status_code=BAD_REQUEST_CODE).return_response_object()

    # Check login for Driver
    elif role_.upper().strip() == DRIVER_ROLE:
        if user_profile.is_driver and Driver.objects.filter(user=user_obj).exists():
            user = authenticate(username=email_, password=password_)
            if user:
                user.userprofile.is_active = True
                user.userprofile.save()
                token = jwt_.create_user_session(user)
                return SuccessResponse(data={'token': token}).return_response_object()
            else:
                return FailureResponse(message='Invalid password',
                                       status_code=BAD_REQUEST_CODE).return_response_object()
        else:
            return FailureResponse(message='Driver Role is not active',
                                   status_code=BAD_REQUEST_CODE).return_response_object()

    # Check login for buyer
    elif role_.upper().strip() == BUYER_ROLE:
        if user_profile.is_buyer:
            user = authenticate(username=email_, password=password_)
            if user:
                user.userprofile.is_active = True
                user.userprofile.save()
                token = jwt_.create_user_session(user)
                return SuccessResponse(data={'token': token}).return_response_object()

            else:
                return FailureResponse(message='Invalid password',
                                       status_code=BAD_REQUEST_CODE).return_response_object()
        else:
            return FailureResponse(message='Buyer Role is not active',
                                   status_code=BAD_REQUEST_CODE).return_response_object()

# add phone number
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True,
                            authentication_level=[BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE])
def add_phonenumber(request):
    try:
        data = get_request_obj(request)
        phone_number = data['phone_number'].lower().strip()
        user_ = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
    
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()
    
    if UserProfile.objects.filter(phone_number=phone_number).exclude(user=user_).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='phone number already in used.').return_response_object()
    
    try:
        UserProfile.objects.filter(user=user_).update(phone_number=phone_number)
        return SuccessResponse(message="phone number added.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="unable to login, try again").return_response_object()





# login with phone number
@decorator_.rest_api_call(allowed_method_list=['POST'])
def login_with_phonenumber(request):
    try:
        data = get_request_obj(request)
        phone_number = data['phone_number'].lower().strip()
        role_ = data['role'].upper().strip()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
    
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()

    if not validate_expected_role(role_):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid role.').return_response_object()
    
    try:
        user_profile_ = UserProfile.objects.get(phone_number=phone_number)
        if role_ == SELLER_ROLE:
            if not user_profile_.is_seller:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='seller role is not active.').return_response_object()
                
        elif role_ == DRIVER_ROLE:
            if not user_profile_.is_driver:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='driver role is not active.').return_response_object()
                
        elif role_ == BUYER_ROLE:
            if not user_profile_.is_buyer:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='buyer role is not active.').return_response_object()
        try:
            user_ = user_profile_.user
            token = jwt_.create_user_session(user_)
            return SuccessResponse(data={'token': token}).return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="unable to login, try again").return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='phone number is not registered.').return_response_object()



@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True,
                          authentication_level=[DRIVER_ROLE, BUYER_ROLE, SELLER_ROLE])
def logout(request):
    user_ = request.user
    try:
        user = UserProfile.objects.get(user=user_)
        user.is_active = False
        user.save()
        try:
            Driver.objects.filter(user=user_).update(is_active=False, is_active_taxi_and_delivery_role=False)
        except:
            pass
        return SuccessResponse(message="logout success").return_response_object()
    except:
        return FailureResponse(message='Unable to logout',
                                   status_code=BAD_REQUEST_CODE).return_response_object()


#check, either new user of old. if old than mathced password.
@decorator_.rest_api_call(allowed_method_list=['POST'])
def check_user_previews_password(request):
    data = get_request_obj(request)
    try:
        email_ = data['email'].lower().strip()
        password_ = data['password']
        role_ = data['role'].upper().strip()
        phone_ = data['phone_number']
        if not validate_email_format(email_):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid email format.').return_response_object()
        
        if not validate_null_values(data):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()
        
        try:
            user_ = User.objects.get(email=email_)
            if role_ == SELLER_ROLE:
                if user_.userprofile.is_seller or Seller.objects.filter(user=user_).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                            message='Seller role is already active on this email.').return_response_object()
                    
            elif role_ == DRIVER_ROLE:
                if user_.userprofile.is_driver or Driver.objects.filter(user=user_).exists():
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                        message='Driver role is already active on this email.').return_response_object()
            else:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='invalid role').return_response_object()
            
            #verify phone number existance
            if UserProfile.objects.filter(phone_number=phone_).exclude(user=user_):
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='phone number already in used.').return_response_object()

            if not user_.check_password(password_):
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                            message='invalid password of previous selected role.').return_response_object()
            else:
                return SuccessResponse(message='new role approval.').return_response_object()
        except:
            return SuccessResponse(message='new user approval.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()


# Buyer Registration
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_buyer(request):
    data = get_request_obj(request)
    try:
        email = data['email'].lower().strip()
        role = data['role'].upper().strip()
        address = data['address']
        password = data['password']
        lat = float(data['lat'])
        lng = float(data['lng'])
        if len(password)<8 or len(password)>20:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="password length should between 8-20 character.").return_response_object()

        if not validate_email_format(email):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid email format.').return_response_object()
        
        if not validate_null_values(data):
            return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                    message="Please fill all the fields.").return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data.").return_response_object()
        
    if not Role.objects.filter(name=role).exists() or role.upper().strip() != BUYER_ROLE:
        return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                message='User role is not valid').return_response_object()
        
    if User.objects.filter(email__iexact=email).exists():
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='email already exists.').return_response_object()
    try:
        try:
            customer = stripe.Customer.create(
                description="This user is created from buyer registeration api.",
                email = email,
            )
            strip_customer_key_ = customer['id']
        except Exception as e:
            print(e)
        
        fistname_ = get_email_first_part(email)
        email_verification_token_ = generate_email_verification_token()
        user_ = User.objects.create_user(email=email, username=email,password=password)
        UserRole.objects.create(user=user_, role=Role.objects.get(name=BUYER_ROLE))
        User_Addresses.objects.create(user=user_, lat=lat, lng=lng, address=address, is_default=True)
        UserProfile.objects.create(user=user_,first_name=fistname_, name=fistname_,is_buyer=True,
                                   email_verification_token=email_verification_token_,strip_customer_key=strip_customer_key_)
        try:
            html_content = get_html_for_email_verification(EMAIL_VERIFICATION_LINK,email_verification_token_)
            subject, from_email, to = 'kwk | Verification', 'fitstarproo@gmail.com', email
            text_content = 'This is an important message.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(e)
    except:
        User.objects.get(email=email).delete()
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                           message='please try again.').return_response_object()
    # Directly login
    user = authenticate(username=email, password=password)
    if user:
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()
    return FailureResponse(status_code=BAD_REQUEST_CODE,
                           message='unable to directly login, try login.').return_response_object()

@decorator_.rest_api_call(allowed_method_list=['GET'])
def email_verification(request):
    try:
        token_ =  request.GET['token']
        UserProfile.objects.filter(email_verification_token=token_).update(is_email_verified=True)
    except Exception as e:
        print(e)
    return redirect('https://kwktech.com/')


# Send verification code to Email for Reset Password
@decorator_.rest_api_call(allowed_method_list=['POST'])
def send_and_resend_email_otp_to_reset_password(request):
    time_now = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
    time_expire = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(seconds=60), "%Y-%m-%d %H:%M:%S")
    try:
        data = get_request_obj(request)
        email = data['email'].lower().strip()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please provide valid data').return_response_object()
        
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please fill all the fields.').return_response_object()

    if not validate_email_format(email):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                           message='Invalid email format.').return_response_object()
    try:
        user = User.objects.get(email=email)
        try:
            reset_object = ResetPassword.objects.get(user=user)
        except:
            reset_object = ResetPassword.objects.create(user=user)
            reset_object.key_expires = time_now
            reset_object.save()
            try:
                reset_object = ResetPassword.objects.get(user=user)
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='please try again.').return_response_object()
            
        if reset_object.key_expires <= utc.localize(parser.parse(time_now)):
            verification_code = generate_six_digits_code()
            html_content = get_html_for_otp(verification_code)
            subject, from_email, to = 'kwk | Verification Code', 'fitstarproo@gmail.com', email
            text_content = 'This is an important message.'
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                reset_object.verification_code = verification_code
                reset_object.key_expires = time_expire
                reset_object.save()
                return SuccessResponse(message='Verification code sent on email').return_response_object()
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable to send email').return_response_object()
        else:
            min = reset_object.key_expires - utc.localize(parser.parse(time_now))
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='Please try after ' + str(min) + " minutes ").return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='invalid email').return_response_object()


# Validate verification code for Reset Password
@decorator_.rest_api_call(allowed_method_list=['POST'])
def validate_reset_password_otp(request):
    try:    
        data = get_request_obj(request)
        verification_code = str(data['verification_code'])
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please provide valid data').return_response_object()
        
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please fill all the fields.').return_response_object()
        
    time_now = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
    try:
        reset_object = ResetPassword.objects.get(verification_code=verification_code)
        if reset_object.key_expires < utc.localize(parser.parse(time_now)):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message='Verfication code expired').return_response_object()
        else:
            return SuccessResponse({"email": reset_object.user.email},
                               message='verificaton code matched').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='Invalid code/expired').return_response_object()


# Reset Password
@decorator_.rest_api_call(allowed_method_list=["POST"])
def create_new_password(request):
    try:    
        data = get_request_obj(request)
        email = data['email']
        password = data['password']
        if len(password)<8 or len(password)>20:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="password length should between 8-20 character.").return_response_object() 
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please provide valid data.').return_response_object()
        
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='please fill all the fields.').return_response_object()
    
    if not validate_email_format(email):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                           message='Invalid email format.').return_response_object()
        
    try:
        user_ = User.objects.get(email=email)
        user_.set_password(password)
        user_.save()
        user_profile = UserProfile.objects.get(user=user_)
        user_profile.is_email_verified = True
        user_profile.save()
        try:
            token = jwt_.create_user_session(user_)
            return SuccessResponse(data={'token': token}).return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='Unable to login').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='Invalid email').return_response_object()



#create instance firebase clouding message token for notifications
@decorator_.rest_api_call(allowed_method_list=['POST'] ,is_authenticated=True, 
                            authentication_level=[DRIVER_ROLE, BUYER_ROLE, SELLER_ROLE])
def create_fcm_device(request):
    data = get_request_obj(request)
    fcm_token = data['fcm_token']
    try:
        device = FCMDevices.objects.update_or_create(user=request.user)
        device[0].fcm_token = fcm_token
        device[0].save()
        if device[1]:
            return SuccessResponse(message='fcm token created successfully').return_response_object()
        else:
            return SuccessResponse(message='fcm token updated successfully').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message="failed to create token").return_response_object()
        
#create bank accont verification on stripe
@decorator_.rest_api_call(allowed_method_list=['POST'] ,is_authenticated=True, 
                            authentication_level=[DRIVER_ROLE, BUYER_ROLE, SELLER_ROLE])
def create_bank_accont_verification(request):
    try:
        data = get_request_obj(request)
        user = request.user
        holder_name = data['holder_name']
        account_object = data['account_object']
        holder_type = data['holder_type']
        country = data['country']
        currency = data['currency']
        account_number = data['account_number']
        routing_number = data['routing_number']
        profile = UserProfile.objects.get(user=user)
        stripe_customer_key = profile.strip_customer_key
        try:
            source = {
                "account_holder_name": holder_name,
                "object":account_object,
                "account_holder_type": holder_type,
                "country": country,
                "currency":currency,
                "account_number":account_number,
                "routing_number":routing_number,#if account number is provided IBAN, than routing number not required
            }
            bank_account = stripe.Customer.create_source(
                                    stripe_customer_key,
                                    source=source,
                                    )
            verify = bank_account.verify(amounts = [32,45]) #32 and 45 cents
            print(verify)
            BankAccountDetails.objects.create(holder_name=holder_name, account_object=account_object, holder_type=holder_type,
                                              country=country, currency=currency, account_number=account_number,status=verify['status'],
                                              routing_number=routing_number, user=user, stripe_source_key= verify['id'])
            return SuccessResponse(message=SUCCESS_CREATED).return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE, 
                               message=SOMETHING_WENT_WRONG).return_response_object()
            #expected response
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE, 
                               message=PROVIDE_VALID_DATA).return_response_object()
        
        
    # stripe_source_key = models.TextField(max_length=255)
    # is_bank_account_verified = models.BooleanField(default=False)
    
        
#Testing api for postman only
@decorator_.rest_api_call(allowed_method_list=['POST'])
def notify_user_testing(request):
    data = get_request_obj(request)
    fcm_token = data['fcm_token']

    message_title = 'Test'
    message_body = 'This is testing notifications.'
    print(list(fcm_token))
    fcm_list = []
    fcm_list.append(fcm_token)
    # msg = send_push(message_title, message_body, list(fcm_token))
    msg = send_push(message_title, message_body, fcm_list)
    return SuccessResponse(message=msg).return_response_object()
        
@decorator_.rest_api_call(allowed_method_list=['POST'],
                         is_authenticated=True, authentication_level=[BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE])
def switch_role(request):
    try:
        user = request.user
        data = get_request_obj(request)
        role = data['role'].upper()
        if role == BUYER_ROLE:
            user.userprofile.is_active = True
            user.userprofile.save()
        elif role == SELLER_ROLE:
            if user.userprofile.is_seller:
                user.userprofile.is_active = True
                user.userprofile.save()
            else:
                return FailureResponse(status_code=PAGE_NOT_FOUND,
                                   message="seller role is not active.").return_response_object()
        elif role == DRIVER_ROLE:
            if user.userprofile.is_driver:
                user.userprofile.is_active = True
                user.userprofile.save()
            else:
                return FailureResponse(status_code=PAGE_NOT_FOUND,
                                   message="driver role is not active.").return_response_object()
        else:
            return FailureResponse(status_code=PAGE_NOT_FOUND,
                                   message="invalid role.").return_response_object()
        token = jwt_.create_user_session(user)
        return SuccessResponse(data={'token': token}).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message="please provide valid data.").return_response_object()
    

#start---------------------------phone number register and login ---------------------------------

'''
# Sent/Resend OTP on Phone Number to login
@decorator_.rest_api_call(allowed_method_list=['POST'])
def send_otp_on_phonenumber_to_login(request):
    try:
        data = get_request_obj(request)
        phone_number = data['phone_number'].lower().strip()
        role_ = data['role'].upper().strip()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
    
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()

    if not validate_expected_role(role_):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid role.').return_response_object()
    
    try:
        user_profile_ = UserProfile.objects.get(phone_number=phone_number)
        if role_ == SELLER_ROLE:
            if not user_profile_.is_seller:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='seller role is not active.').return_response_object()
                
        elif role_ == DRIVER_ROLE:
            if not user_profile_.is_driver:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='driver role is not active.').return_response_object()
                
        elif role_ == BUYER_ROLE:
            if not user_profile_.is_buyer:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='buyer role is not active.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='phone number is not registered.').return_response_object()
    
    try:
        verification_code = generate_six_digits_code()
        time_now = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")
        time_expire = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(seconds=PHONE_NUMBER_OTP_EXPIRY_IN_SECONDS), "%Y-%m-%d %H:%M:%S")

        phone_obj = PhoneNumbers.objects.get(phone_number=phone_number)
        if phone_obj.key_expires < utc.localize(parser.parse(time_now)):

            message_to_broadcast = ("kwkDrop Verification Code : " + verification_code)
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(to=phone_number, from_=TWILIO_NUMBER, body=message_to_broadcast)

            phone_obj.verification_code = verification_code
            phone_obj.key_expires = time_expire
            phone_obj.save()
            return SuccessResponse(data={'phone_number': phone_number},
                                    message='OTP resent').return_response_object()
        else:
            min = phone_obj.key_expires - utc.localize(parser.parse(time_now))
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='Please try after ' + str(min) + " minutes ").return_response_object()
    except:
        try:
            message_to_broadcast = ("kwkDrop Verification Code : " + verification_code)
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(to=phone_number, from_=TWILIO_NUMBER, body=message_to_broadcast)
            PhoneNumbers.objects.create(verification_code=verification_code, key_expires=time_expire,
                                            phone_number=phone_number)
            return SuccessResponse(data={'phone_number': phone_number},
                                    message='OTP sent').return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="Unable to send otp").return_response_object()


# Validate OTP and Add Mobile number
@decorator_.rest_api_call(allowed_method_list=["POST"])
def validate_phonenumber_otp_and_login_directly(request):
    try:
        data = get_request_obj(request)
        otp = data['otp']
        phone_number_ = data['phone_number']
        user_ = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
        
    if not validate_null_values(data):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()

    time_now = dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d %H:%M:%S")

    try:
        phone_number_object = PhoneNumbers.objects.get(phone_number=phone_number_, verification_code=otp)
        if phone_number_object.key_expires < utc.localize(parser.parse(time_now)):
            phone_number_object.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE, message='OTP expired').return_response_object()
        else:
            try:
                user_profile_ = UserProfile.objects.get(phone_number=phone_number_)
                user_ = user_profile_.user
                token = jwt_.create_user_session(user_)
                return SuccessResponse(data={'token': token}).return_response_object()
                
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable to login, try again').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message='Invalid OTP').return_response_object()'''
        
#----------------------------end--------------------------