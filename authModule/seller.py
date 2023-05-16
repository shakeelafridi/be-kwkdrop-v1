from kwk.settings import *
import pytz
from utilities.reuseableResources import *
from utilities.constants import *
import stripe

utc = pytz.UTC
decorator_ = DecoratorHandler()
jwt_ = JWTClass()
stripe.api_key = STRIP_SECRET_KEY



#register seller and its shop
@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_seller(request):
    response_errors = ""
    is_errors = False
    try:
        data = get_request_obj(request)
        email_ = data['email'].lower().strip()
        password_ = data['password']
        role_ = data['role'].upper().strip()
        shop_name_ = data['shop_name']
        phone_ = data['phone']
        address_ = data['address']
        lat_ = float(data['lat'])
        lng_ = float(data['lng'])
        shop_images_ = data['shop_images']
        # 362 24/7 Always open in whole year
        is_always_open_ = data['is_always_open']
        # open and close time for whole week
        week_times_ = data['week_times']
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()
    
    #Validata null address
    if not validate_null_address(lat_, lng_, address_):
        response_errors = concat_errors_string(response_errors, 'please set shop address')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                             message='please set shop address').return_response_object()
    
    #validate email format
    if not validate_email_format(email_):
        response_errors = concat_errors_string(response_errors, 'invalid email format.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                             message='invalid email format.').return_response_object()
    
    #validate password
    if not validate_password(password_):
        response_errors = concat_errors_string(response_errors, 'password should between 8-20 digits.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                         message='password should between 8-20 digits.').return_response_object()
    
    #if request by ios(Form) than convert the array into json
    if request.POST:
        week_times_ = json.loads(week_times_)
        shop_images_ = json.loads(shop_images_)
        
    #validate null fields
    if not is_always_open_:
        if not validate_null_values(data):
            print(week_times_)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please fill all the fields.').return_response_object()
        
    #validate shop hours that has set for week.
    if not is_always_open_:
        week_times_check_ = validate_week_days(week_times_)
        if not week_times_check_:
            response_errors = concat_errors_string(response_errors, 'Shop hours is not valid')
            is_errors = True
            # return FailureResponse(status_code=BAD_REQUEST_CODE, message='Shop hours is not valid').return_response_object()
    
    #validate seller role
    role_ = role_.upper().strip()
    role = Role.objects.filter(name__iexact=role_).last()
    if not role or role_ != SELLER_ROLE:
        response_errors = concat_errors_string(response_errors, 'User role is not valid')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    if is_errors:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=response_errors).return_response_object()
    
    #verification: 
    # 1. validate previews role password if the it is join as seller
    # 2. validate if the same seller do rejoin as seller
    # 3. if above conditions failed than create new seller
    try:
        user_ = User.objects.get(email=email_)
        if user_:
            if user_.userprofile.is_seller or Seller.objects.filter(user=user_).exists():
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='Seller role is already active on this email.').return_response_object()
                
            #verify phone number existance
            if UserProfile.objects.filter(phone_number=phone_).exclude(user=user_).exists():
                print('old user')
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='phone number already in used.').return_response_object()

            if not user_.check_password(password_):
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                            message='invalid password of previous selected role.').return_response_object()
    except Exception as e:
        print('new user')
        #verify phone number existance
        if UserProfile.objects.filter(phone_number=phone_).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='phone number already in used.').return_response_object()
        print(e)

    #get or create user
    #1. get user if previews user join as a seller
    #2. create fresh user
    try:
        try:
            u_profile = UserProfile.objects.get(user=user_)
        except:
            try:
                try:
                    customer = stripe.Customer.create(
                        description="This user is created from buyer registeration api.",
                        email = email_,
                    )
                    strip_customer_key_ = customer['id']
                except Exception as e:
                    print(e)
                
                first_name_ = get_email_first_part(email_)
                user_ = User.objects.create(email=email_, username=email_, first_name=first_name_)
                user_.set_password(password_)
                user_.save()
                u_profile = UserProfile.objects.create(user=user_, name=first_name_, first_name=first_name_,
                                                       phone_number=phone_,strip_customer_key = strip_customer_key_)
                UserRole.objects.create(user=user_, role=Role.objects.get(name=BUYER_ROLE))
                user_created_flag = True
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable to create user, try agian.').return_response_object()
        try:
            UserProfile.objects.filter(user=user_).update(address = address_, is_seller=True,
                                                          is_buyer=True, is_email_verified=True)
            
            # u_profile.address=address_,
            # u_profile.is_seller=True,
            # u_profile.is_buyer=True,
            # u_profile.is_email_verified=True,
            # if phone_:
            #     u_profile.phone_number = phone_
            # u_profile.save()
                
            role_obj_ = UserRole.objects.create(user=user_, role=Role.objects.get(name=role_))
            try:
                User_Addresses.objects.filter(user=user_).update(is_default=False)
            except Exception as e:
                print(e)
            User_Addresses.objects.create(user=user_, lat=lat_, lng=lng_, address=address_)
            seller_obj_ = Seller.objects.create(user=user_, profile=u_profile, role=role_obj_)
            shop_obj_ = Shop.objects.create(lat=lat_, lng=lng_, shop_address=address_, shop_name=shop_name_,
                                            is_always_open=is_always_open_, phone_number=phone_, seller=seller_obj_)
            
            if not is_always_open_:
                for obj in week_times_:
                    shp_ = SellerShopHour.objects.create(shop=shop_obj_, day=obj['name'])
                    sht_ = ShopHourTiming.objects.create(hour=shp_, is_open_24=obj['is_24hours'], is_close=obj['is_off'])
                    if not obj['is_24hours'] and not obj['is_off']:
                        sht_.open_time = obj['open_time']
                        sht_.close_time = obj['close_time']
                        sht_.save()

            if len(shop_images_) > 0:    
                for i in range(len(shop_images_)):
                    Shop_images.objects.create(shop=shop_obj_, shop_image_url=shop_images_[i]['url'])

            token = jwt_.create_user_session(user_)
            return SuccessResponse(data={'token': token}).return_response_object()
        except Exception as e:
            print(e)
            #if new user created but unable to create driver
            if user_created_flag:
                user_.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='unable to create seller, try agian.').return_response_object()
        
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unable to create user, try agian.').return_response_object()
