from seller.reuselable_resources import notify_users_on_order_updates
from buyer.buyer_reusable_resources import get_data_in_list
from django.db.models.aggregates import Sum
from driver.models import DriverEarning
from re import T
from authModule.models import DriverRoles
from os import stat
from utilities.models import USState
from utilities.reuseableResources import *
from authModule.models import DriverRadiusSettings, Driver
from utilities.jwt import JWTClass
from utilities.constants import *
from buyer.serializer import GetOrderDetailsSerializer
from .serializer import GetDriverEarningSerializers, GetListOfAssignOrderToDriverForAcceptence
import datetime as dt

decorator_ = DecoratorHandler()
jwt_ = JWTClass()

@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def driver_checker_verification_status(request):
    user = request.user
    driver_checkr_object = Driver_checker.objects.get(driver__user=user)
    report_id = driver_checkr_object.checker_report_id
    status = check_report_status(report_id)
    return SuccessResponse(message="Info", data={'checkr_status':status}).return_response_object()


@decorator_.rest_api_call(allowed_method_list=['POST', 'GET'], is_authenticated=True, authentication_level=DRIVER_ROLE)
def set_driver_radius(request):
    try:
        driver_ = Driver.objects.get(user=request.user)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="invalid driver.").return_response_object()
    drs_, created = DriverRadiusSettings.objects.get_or_create(driver=driver_)

    if request.method == 'POST':
        data = get_request_obj(request)

        is_driver_current_location = data['is_driver_current_location']
        latitude = data['latitude'] if 'latitude' in data else 0
        longitude = data['longitude'] if 'longitude' in data else 0
        radius = data['radius'] if 'radius' in data else 0

        drs_.is_current_location = is_driver_current_location

        if not is_driver_current_location:
            drs_.lat = float(latitude)
            drs_.lng = float(longitude)
            drs_.radius = float(radius)
            drs_.save()
        return SuccessResponse(message='Information Updated').return_response_object()
    elif request.method == 'GET':
        radius_range_list = []
        try:
            driver_role = DriverRoles.objects.filter(driver=driver_,is_active=True).first()
            if driver_role.name.upper() == PEDESTRIAN:
                radius_range_list.append({'meters':1000,'km':1})
            else:
                # get_driver_vehicle_type = Vehicle.objects.get(driver = driver_)
                # if not get_driver_vehicle_type.vehicle_type.type.upper() == PEDESTRIAN:
                radius_range_list.append({'meters':1000,'km':1})
                radius_range_list.append({'meters':2000,'km':2})
                radius_range_list.append({'meters':3000,'km':3})
                radius_range_list.append({'meters':4000,'km':4})
                radius_range_list.append({'meters':5000,'km':5})
        except Exception as e:
            print(e)
            
            # radius_range_list.append({'meters':300,'km':0.3})
            # radius_range_list.append({'meters':400,'km':0.4})
            # radius_range_list.append({'meters':500,'km':0.5})
        data_ = {
            'latitude': drs_.lat,
            'longitude': drs_.lng,
            'radius': drs_.radius,
            'is_driver_current_location': drs_.is_current_location,
            'radius_range_list':radius_range_list
        }
        return SuccessResponse(message='Info', data=data_).return_response_object()


#Get US states
@decorator_.rest_api_call(allowed_method_list=['GET'])
def get_states_and_vehicle_type(request):
    states = []
    vehicle_type_list = []
    get_states = USState.objects.all()
    for state in get_states:
        states.append({'name':state.name, 'abbr':state.abbr})
    get_vehicle_types = VehicleType.objects.all()
    for vehicle_type in get_vehicle_types:
        vehicle_type_list.append({'id':vehicle_type.id, 'type':vehicle_type.type})
    return SuccessResponse(message='Info', data={
                            'states':states,
                            'vehicle_types':vehicle_type_list}).return_response_object()


#retreive or update driver status
@decorator_.rest_api_call(allowed_method_list=['GET','POST'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def driver_desktop_and_status_ru(request):
    get_driver_status = False
    is_both_roles_active = False
    orders_notification_counter = 0
    others_notification_counter = 2
    is_checkr_verified = False
    is_bank_account_verified = False
    try:
        user_ = request.user
        driver_ = Driver.objects.get(user=user_)
        user_profile_ = UserProfile.objects.get(user=user_)
        full_name_ = user_profile_.name
        get_driver_status = driver_.is_active
        is_both_roles_active = driver_.is_active_taxi_and_delivery_role
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid user.').return_response_object()
    try:
        get_driver_role_object_ = DriverRoles.objects.get(driver=driver_, is_active=True)
        get_driver_active_role = ''.join(get_driver_role_object_.role.name)
        
    except:
        get_driver_active_role = ''
    if request.method == "POST":
        data = get_request_obj(request)
        try:
            is_active_ = data['is_active']
            role_ = data['role'].upper().strip()
            is_both_ = data['is_both_taxi_and_delivery']
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='please provide valid data').return_response_object()
        try:
            if not is_active_:
                pass
            elif not is_both_:
                if (role_ == TAXI_ROLE or role_ == DELIVERY_ROLE):
                    role_object_ = Role.objects.get(name=role_)
                else:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='invalid role/select role '+ role_).return_response_object()
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='role not found').return_response_object()

        # if not driver_.is_verified_from_checker:
        #     return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                                 message='kindly wait until we verify your backgrounds.').return_response_object()
        
        if not is_active_:
            driver_.is_active = False
            driver_.is_active_taxi_and_delivery_role = False
        elif is_active_:
            driver_.is_active = True
            if is_both_:
                driver_.is_active_taxi_and_delivery_role = True
            else:
                driver_.is_active_taxi_and_delivery_role = False
                try:
                    role_objects_ = DriverRoles.objects.filter(driver=driver_)
                    for row_role in role_objects_:
                        row_role.is_active = False
                        row_role.save()
                except:
                    pass
                driver_role_object_, created_ = DriverRoles.objects.update_or_create(driver=driver_, role=role_object_,
                                                                                    defaults={'is_active': True},)
                if not created_:
                    get_driver_active_role = str(driver_role_object_.role.name)
                else:
                    get_driver_active_role = str(created_.role.name)
        try:
            driver_.save()
            get_driver_status = driver_.is_active
            is_both_roles_active = driver_.is_active_taxi_and_delivery_role
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="unable to update status.").return_response_object()
    
    #count order
    try:
       orders_notification_counter = AssignOrderToDriverForAcceptence.objects.filter(driver__user=user_).count()
    except Exception as e:
        print(e)
        
    #get checkr status, now we hit the checkr apis to have that record, later when create
    #scheduler or cronjob, update the model using scheduler. Here we get load the checkr verification from models.
    try:
        user = request.user
        driver_checkr_object = Driver_checker.objects.get(driver__user=user)
        report_id = driver_checkr_object.checker_report_id
        status = check_report_status(report_id)
        if status == CLEAR:
            is_checkr_verified = True
    except Exception as e:
        print(e)
    
    return SuccessResponse(
                        data={'full_name':full_name_,
                                'is_active':get_driver_status,
                                'active_role': get_driver_active_role,
                                'is_both_roles_active':is_both_roles_active,
                                'is_checkr_verified':is_checkr_verified,
                                'is_bank_account_verified':is_bank_account_verified,
                                'orders_notification_counter':orders_notification_counter,
                                'others_notification_counter':others_notification_counter}).return_response_object()
    

#Get list of orders for driver that system suggested him base on nearby location
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def get_orders_list_for_driver(request):
    try:
        user_ = request.user
        driver_ = Driver.objects.get(user=user_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid driver').return_response_object()
    try:
        assign_order_list_ = AssignOrderToDriverForAcceptence.objects.filter(driver=driver_).order_by('created_at').reverse()
        assign_list = GetListOfAssignOrderToDriverForAcceptence(assign_order_list_, many=True).data
        return SuccessResponse(data={'assign_list':assign_list}).return_response_object()

    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='no orders found.').return_response_object()
        

#Accept or Reject order by driver
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def accpet_or_reject_order_by_driver(request):
    try:
        user_list = []
        data = get_request_obj(request)
        assign_order_id_ = int(data['assign_order_id'])
        is_accept = data['is_accept']
        user_ = request.user
        driver_ = Driver.objects.get(user=user_)
        #check if driver has already assigned a task
        # if AssignOrderToDriverForAcceptence.objects.filter(driver=driver_,is_order_accepted=True).exists() and is_accept:
        #     return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                             message='kindly complete assigned job first.').return_response_object()
        try:
            #assign driver when accept order
            if is_accept:
                try:
                    assign_order_ = AssignOrderToDriverForAcceptence.objects.get(id=assign_order_id_)
                    order_object = assign_order_.order
                    #get list of assigned orders to driver
                    get_assigned_list_ = AssignOrderListToDriver.objects.filter(assign_order=assign_order_)
                    for list_object in get_assigned_list_:      
                        list_object.assign_order.is_order_accepted = True
                        list_object.assign_order.save()
                        
                    #get first assigned driver to order.
                    queue_assinged_object = AssignOrderToDriverForAcceptence.objects.filter(order=order_object, is_order_accepted=True).latest('updated_at')
                    #if driver not assigned to order than 'False' the  acception
                    if not queue_assinged_object.driver == driver_:
                        assign_order_.delete()
                        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                               message='job has assigned to another driver using queue system.').return_response_object()
                    #if driver has first to accept the order than assign order
                    else:
                        time_now = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(seconds=THREE_MINTS_IN_SECONDS), "%Y-%m-%d %H:%M:%S")
                        for list_object in get_assigned_list_:
                            #update 'AssignOrderToDriverForAcceptence' attributes
                            list_object.assign_order.is_order_accepted = True
                            list_object.assign_order.save()
                            #update 'ShopOrder' Attributes
                            list_object.order.driver = driver_
                            list_object.order.is_driver_accepted = True
                            list_object.order.order_status = ACCEPTED
                            list_object.order.save()
                            user_list.append(list_object.order.shop.seller.user)
                        #update 'Order' Attributes
                        order_id = order_object.id
                        user_list.append(order_object.buyer)
                        Order.objects.filter(id=order_id).update(driver_accepted_time=time_now,
                                                                 is_drivers_accepted=True,
                                                                 order_status = ACCEPTED
                                                                 )
                        message_title_ = "Order #"+str(order_id)+" Accepted"
                        message_body_ = "Order #"+str(order_id)+" accepted by Driver."
                        notify_users_on_order_updates(order_object, message_title_, message_body_, users_roles=[BUYER_ROLE, SELLER_ROLE])
                        set_firebase_order_node(order_object, ACCEPTED)
                        set_firebase_order_tracking_info(order_object)
                        AssignOrderToDriverForAcceptence.objects.filter(order=order_object).delete() #.exclude(id=assign_order_id_).delete()
                        return SuccessResponse(message='order accepted.').return_response_object()                
                except Exception as e:
                    print(e)
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='unable accept ride, try again.').return_response_object()
                
            #do not show the same order when driver reject order.
            else:
                AssignOrderToDriverForAcceptence.objects.filter(id=assign_order_id_).delete()
                return SuccessResponse(message='order rejected.').return_response_object() 
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid request for to assign order.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()


#Get order details that has been own by driver    
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_order_details_for_driver(request):
    try:
        user_ = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid user.').return_response_object()
    try:
        driver_ =  Driver.objects.get(user=user_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid driver.').return_response_object()
    try:
        get_order_objects = ShopOrder.objects.filter(driver=driver_)
        order_serializer_ = GetOrderDetailsSerializer(get_order_objects,many=True).data
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='no order found.').return_response_object()
    
    
#Get driver completed order history  
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def get_driver_completed_order_history(request):
    try:
        user_ = request.user
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid user.').return_response_object()
    try:
        driver_ =  Driver.objects.get(user=user_)
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='invalid driver.').return_response_object()
    try:
        get_order_objects = ShopOrder.objects.filter(driver=driver_, order_status=COMPLETED).order_by('created_at').reverse()
        order_serializer_ = GetOrderDetailsSerializer(get_order_objects,many=True).data
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except:
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='no order found.').return_response_object()
    

#leave order at door step and take picture and update db.(Driver)
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def order_doop_step_delivered(request):
    try:
        data = get_request_obj(request)
        user_ = request.user
        order_id = int(data['order_id'])
        images = data['images']
        for index in images:
            str(index['url'])
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    try:
        order_object = Order.objects.get(id=order_id)
        if order_object.order_status == DELIVERED:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                           message='order is already delivered.')
        #create records of door step
        create_object = OrderDoorStepDelivered.objects.create(order_id=order_object,images=images)
        get_order_door_step_images = create_object.images
        Order.objects.filter(id=order_id).update(order_status=DELIVERED)
        #create driver earning records
        driver = Driver.objects.get(user=user_)
        get_, created = DriverEarning.objects.get_or_create(driver=driver,order=order_object)
        if not created:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='order is already delivered.')
        AssignOrderToDriverForAcceptence.objects.filter(order=order_object).delete()
        try:#notify buyer
            message_title_ = "Order "+str(DELIVERED)+"."
            message_body_ = "Your order #"+str(order_object.id)+" has been "+str(DELIVERED)+" at door step."
            notify_user(order_object.buyer, message_title_, message_body_)
        except Exception as e:
            print(e)
        return SuccessResponse(data={"images":get_order_door_step_images},message='succesed.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="failed, please try agian.").return_response_object()
        

#Driver orders history
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def get_driver_order_history(request):
    try:
        data = get_request_obj(request)
        user = request.user
        order_status_ = data['order_status'].strip().lower()
        if not order_status_ in driver_order_list_status:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="invalid order status").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    try:
        get_orders_objects = ShopOrder.objects.filter(driver__user=user).values_list('order')
        order_list = get_data_in_list(get_orders_objects)
        if order_status_ == PROGRESS:
            get_order_objects = Order.objects.filter(id__in=order_list,order_status__in=progress_order_list).order_by('created_at').reverse()
        else:
            get_order_objects = Order.objects.filter(id__in=order_list,order_status=order_status_).order_by('created_at').reverse()
        print(get_order_objects)
        order_serializer_ = GetOrderDetailsSerializer(get_order_objects,many=True).data                    
        return SuccessResponse(data={'order_details':order_serializer_},
                                    message='order information.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,    
                                message='no order found.').return_response_object()


#Driver revenue model
@decorator_.rest_api_call(allowed_method_list=['GET'], is_authenticated=True, authentication_level=[DRIVER_ROLE])
def get_driver_earning(request):
    try:
        data = get_request_obj(request)
        user = request.user
        try:
            sum_of_total_earning = DriverEarning.objects.filter(driver__user=user).aggregate(Sum('order__delivery_fee'))
            sum_of_tip = DriverEarning.objects.filter(driver__user=user).aggregate(Sum('tip'))
            total_earning = float(sum_of_total_earning['order__delivery_fee__sum'])+float(sum_of_tip['tip__sum'])
            earning_objects = DriverEarning.objects.filter(driver__user=user).order_by('created_at').reverse()
            earning_history = GetDriverEarningSerializers(earning_objects, many=True).data
            return SuccessResponse(data = {
                'total_earning':total_earning,
                'earning_history' : earning_history
            }).return_response_object()
        except Exception as e:
            return SuccessResponse(message='not details found.').return_response_object()
            
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data.").return_response_object()


# Get us states from below link or /project/utilities/US_states.json
# https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_titlecase.json
# @decorator_.rest_api_call(allowed_method_list=['POST'])
# def insert_US_states(request):    
#     data = get_request_obj(request)
#     data = data['states']
#     for i in range(len(data)):
#         USState.objects.create(name=data[i]['name'], abbr=data[i]['abbreviation'])
#     return SuccessResponse(message='states added successfully').return_response_object()




    





