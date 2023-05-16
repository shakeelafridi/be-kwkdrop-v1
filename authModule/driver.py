import pytz
from kwk.settings import *
from utilities.reuseableResources import *
from datetime import datetime
import stripe

utc = pytz.UTC
decorator_ = DecoratorHandler()
jwt_ = JWTClass()
stripe.api_key = STRIP_SECRET_KEY


@decorator_.rest_api_call(allowed_method_list=['POST'])
def register_driver(request):
    response_errors = ""
    is_errors = False
    data = get_request_obj(request)
    try:
        #Persnol and other detials
        email_ = data['email'].lower().strip()
        password_ = data['password']
        role_ = data['role'].upper().strip()
        first_name_ = data['first_name']
        middle_name_ = data['middle_name']
        last_name_ = data['last_name']
        full_name_ = first_name_+' '+last_name_
        phone_ = data['phone']
        zip_code_ = data['zip_code']
        dob_ = data['dob']
        img_url = data['image_url']
        social_security_number_ = data['social_security_number']
        # lat_ = data['lat']
        # lng_ = data['lng']
        #Vehicle details
        vehicle_type_ = int(data['vehicle_type'])
        vehicle_make_ = data['vehicle_make']
        vehicle_color_ = data['vehicle_color']
        vehicle_number_ = data['vehicle_number']
        #Auto insurance details
        auto_insurance_number_ = data['auto_insurance_number']
        auto_insurance_expiry_ = data['auto_insurance_expiry']
        #License details
        license_state_ = data['license_state']
        license_number_ = data['license_number']
        license_exp_date_ = data['license_exp_date']
        #Bank card details
        # name_of_card = data['name_of_card']
        # card_number = data['card_number']
        # expiry_date = data['expiry_date']
        # cvv_number = data['cvv_number']
        # billing_address = data['billing_address']
        # is_save = data['is_save']
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="please provide valid data.").return_response_object()

    #Validataions
    role = Role.objects.filter(name__iexact=role_).last()
    if not role and role_ != DRIVER_ROLE:
        response_errors = concat_errors_string(response_errors, 'User role is not valid.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE, message='User role is not valid').return_response_object()
    
    #validate checkr basic required fields
    if not checkr_basic_data_null_validation(first_name_, last_name_, 
                                                email_, dob_, phone_, social_security_number_, zip_code_):
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                            message='required fields: first name, last name, email, dob, phone, ssn, zip').return_response_object()

    #email format validation
    if not validate_email_format(email_):
        response_errors = concat_errors_string(response_errors, 'invalid email format.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                        message='invalid email format').return_response_object()

    #password validation
    if not validate_password(password_):
        response_errors = concat_errors_string(response_errors, 'password length should between 8-20.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                     message='password length should between 8-20.').return_response_object()
    
    
    try:#date of birth validation
        dob_ = datetime.strptime(dob_, '%Y-%m-%d')
        #validate age that should greater than 21 for driver.
        if not validate_driver_age(dob_):
            response_errors = concat_errors_string(response_errors, 'age should equal or greater than 21.')
            is_errors = True
            # return FailureResponse(status_code=BAD_REQUEST_CODE,
            #                     message='age should equal or greater than 21.').return_response_object()
    except:
        response_errors = concat_errors_string(response_errors, 'invalid DOB format.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                        message='invalid DOB format.').return_response_object()
        
    #social security number validation
    if not validate_ssn(social_security_number_):
        response_errors = concat_errors_string(response_errors, 'please provide valid SSN.')
        is_errors = True
        # return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                        message='please provide valid SSN.').return_response_object()
        
    if is_errors:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=response_errors).return_response_object()
        
    #validate type of vehicle or padestrain
    try:
        vehicle_type_ = VehicleType.objects.get(id=vehicle_type_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="invalid vehicle type").return_response_object()

    #if not padestrian
    if not vehicle_type_.type.upper().strip() == PEDESTRIAN:
        try:#license expiry date and auto insurance expiry date format validation
            license_exp_date_ = datetime.strptime(license_exp_date_, '%Y-%m-%d')
            auto_insurance_expiry_ = datetime.strptime(auto_insurance_expiry_, '%Y-%m-%d')
            
            if not validate_driver_info(auto_insurance_number_, vehicle_number_, license_number_):
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='auto insurance number/vehicle number/license number should not empty').return_response_object()
            
            if Driver.objects.filter(auto_insurance_number__iexact=auto_insurance_number_).exists():
                response_errors = concat_errors_string(response_errors, 'This auto insurance number already exists.')
                is_errors = True
            # return FailureResponse(status_code=BAD_REQUEST_CODE,
            #                        message='This auto insurance number already exists.').return_response_object()

            if Vehicle.objects.filter(vehicle_number__iexact=vehicle_number_).exists():
                response_errors = concat_errors_string(response_errors, 'This vehicle number already exists.')
                is_errors = True
                # return FailureResponse(status_code=BAD_REQUEST_CODE,
                #                        message='This vehicle number already exists.').return_response_object()

            if License.objects.filter(license_number__iexact=license_number_).exists():
                response_errors = concat_errors_string(response_errors, 'This License number already exists.')
                is_errors = True
                # return FailureResponse(status_code=BAD_REQUEST_CODE,
                #                        message='This License number already exists.').return_response_object()
                    
        except Exception as e:
            print(e)
            response_errors = concat_errors_string(response_errors, 'expiry license/auto insurance expiry date foramat is not vaild.')
            is_errors = True
            # return FailureResponse(status_code=BAD_REQUEST_CODE,
            #                    message='expiry license/auto insurance expiry date foramat is not vaild').return_response_object()

    if Driver.objects.filter(social_security_number=social_security_number_).exists():
        response_errors = concat_errors_string(response_errors, 'This social security number already exists.')
        is_errors = True
    # return FailureResponse(status_code=BAD_REQUEST_CODE,
    #                        message='This social security number already exists.').return_response_object()

    if is_errors:
        return FailureResponse(status_code=BAD_REQUEST_CODE, message=response_errors).return_response_object()
    
    # verification: 
    # 1. validate previews role password if the it is join as driver
    # 2. validate if the same driver do rejoin as driver
    # 3. if above conditions failed than create new driver
    try:
        user_ = User.objects.get(email=email_)
        if user_:
            if user_.userprofile.is_driver or Driver.objects.filter(user=user_).exists():
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='Driver role is already active on this email.').return_response_object()

            #verify phone number existance for existance user but having different role.
            if UserProfile.objects.filter(phone_number=phone_).exclude(user=user_).exists():
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='phone number already in used.').return_response_object()

            if not user_.check_password(password_):
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                            message='invalid password of previous selected role.').return_response_object()
    except Exception as e:
        #verify phone number existance for new user
        print(e)
        if UserProfile.objects.filter(phone_number=phone_).exists():
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                               message='phone number already in used.').return_response_object()
            

    if not vehicle_type_.type.upper().strip() == PEDESTRIAN:
        #middle name optional, set False if null
        if not middle_name_:
            middle_name_for_checkr = False
        else:
            middle_name_for_checkr = middle_name_
        #candiate data that need to send to checkr
        candidate_data = {
            'first_name': first_name_,
            'middle_name': middle_name_for_checkr,
            'last_name': last_name_,
            'email': email_,
            'phone': phone_,
            'zipcode': zip_code_,
            'dob': dob_,
            'ssn': social_security_number_,
            'driver_license_number': license_number_,
            'driver_license_state': license_state_,
            'copy_requested': 'true'
        }
        #Request for candidate checkr dat
        candidate_response, response_status = create_candidate(candidate_data)
        if not response_status:
            candidate_response = candidate_response.json()
            if type(candidate_response['error']) != type("string"):
                candidate_response['error'] = "@".join(candidate_response['error'])
            return FailureResponse(status_code=BAD_REQUEST_CODE, message=candidate_response['error']).return_response_object()

        candidate_response = candidate_response.json()
        candidate_id_ = candidate_response['id']
        #Request for generate candidate report
        candidate_report_data = {
            'package': CHECKER_PACKAGE,
            'candidate_id': candidate_id_
        }
        candidate_report_response, response_status = create_report(candidate_report_data)
        if not response_status:
            candidate_report_response = candidate_report_response.json()
            if type(candidate_report_response['error']) != type("string"):
                candidate_report_response['error'] = "@".join(candidate_report_response['error'])
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message=candidate_report_response['error']).return_response_object()
        candidate_report_response = candidate_report_response.json()
        candidate_report_id_ = candidate_report_response['id']
        
    
    try:
        try:
            u_profile = user_.userprofile
        except:
            try:
                try:
                    customer = stripe.Customer.create(
                        description="This user is created from driver registeration api.",
                        email = email_,
                    )
                    strip_customer_key_ = customer['id']
                except Exception as e:
                    print(e)
                
                user_ = User.objects.create(email=email_, username=email_, first_name=first_name_)
                user_.set_password(password_)
                user_.save()
                u_profile = UserProfile.objects.create(user=user_,phone_number = phone_, 
                                                       strip_customer_key = strip_customer_key_)
                UserRole.objects.create(user=user_, role=Role.objects.get(name=BUYER_ROLE))
                user_created_flag = True
            except:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable to create user, try agian.').return_response_object()
        try:
            u_profile.is_driver = True
            u_profile.is_buyer = True
            u_profile.name = full_name_
            u_profile.first_name = first_name_
            u_profile.last_name = last_name_
            u_profile.middle_name = middle_name_
            u_profile.is_email_verified=True

            # if phone_:
            #     u_profile.phone_number = phone_
            if img_url:
                u_profile.profile_image_url = img_url
            u_profile.zip_code = zip_code_
            u_profile.save()

            role_obj_ = UserRole.objects.create(user=user_, role=role)
            driver_obj = Driver.objects.create(social_security_number = social_security_number_,
                                                profile=u_profile, role=role_obj_,user=user_)
            
            
            #save vehicle and others records of driver if not padestrain
            if vehicle_type_.type.upper().strip() == PEDESTRIAN:
                DriverRoles.objects.create(name=PEDESTRIAN, driver=driver_obj, is_active=True)
            
            if not vehicle_type_.type.upper().strip() == PEDESTRIAN:
                driver_obj.auto_insurance_expiry = auto_insurance_expiry_
                driver_obj.auto_insurance_number = auto_insurance_number_
                driver_obj.save()
                Driver_checker.objects.create(driver=driver_obj, checker_driver_id=candidate_id_,
                                                checker_report_id=candidate_report_id_)
                License.objects.create(driver=driver_obj, license_state=license_state_, license_number=license_number_,
                                        license_exp_date=license_exp_date_)
                Vehicle.objects.create(driver=driver_obj, vehicle_type=vehicle_type_, vehicle_make=vehicle_make_,
                                vehicle_number=vehicle_number_, vehicle_color=vehicle_color_)
                DriverRoles.objects.create(name=DRIVER_ROLE, driver=driver_obj, is_active=True)
                # Bank_card_detail.objects.create(name_of_card=name_of_card, card_number=card_number, expiry_date=expiry_date,
                #                                 cvv_number=cvv_number, billing_address=billing_address, is_save=is_save,
                #                                 user=user_)
            
            token = jwt_.create_user_session(user_)
            return SuccessResponse(data={'token': token}).return_response_object()
        except Exception as e:
            print(e)
            #if new user created but unable to create driver(Exception occured)
            if user_created_flag:
                user_.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable create driver, try again.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="unexpected error. try again.").return_response_object()