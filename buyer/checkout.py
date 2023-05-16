from django.core.mail import message
from seller.reuselable_resources import notify_users_on_order_updates
from buyer.models import BuyerAppliedCoupon
from kwk.settings import STRIP_SECRET_KEY
from seller.models import AssignOrderToDriverForAcceptence, Coupon, Delivery_Options, Delivery_Scheduling, Order, Order_Items, Propane, ShopOrder, Shop_Product
from utilities.RequestHandler import DecoratorHandler
from buyer.buyer_reusable_resources import assign_drivers_to_order, promocode_verification, reiview_shops_and_product, shops_and_product_structure_validation
from utilities.reuseableResources import get_delivery_and_service_charges, get_request_obj, set_firebase_order_node, set_firebase_order_tracking_info
from utilities.ResponseHandler import FailureResponse, SuccessResponse
from authModule.models import Shop, UserProfile, User_Addresses
from utilities.constants import ACCEPTED, BAD_REQUEST_CODE, BUYER_ROLE, DISPUTED, PENDING, PRODUCT, PROPANE, SCHEDULED, SELLER_ROLE, SUCCESS_RESPONSE_CREATED
decorator_ = DecoratorHandler()
import datetime as dt
import stripe
stripe.api_key = STRIP_SECRET_KEY
from rest_framework import status
from payments.models import StripeOrderPaymentIntent
from payments.reuseable_resources import calculate_main_order_amount, discount_formula


#validate checkout data
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def validate_checkout(request):
    total_payment_ = 0
    try:#check already placed order
        buyer_ = request.user
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid user').return_response_object()
    try:#validate request structure
        data = get_request_obj(request)
        data = data['checkout']
        shops = data['shops']
        is_promocode_verified = data['is_promocode_verified']
        if is_promocode_verified:
            promocode = data['promocode']
            is_verified, promocode_data = promocode_verification(promocode)
            if not is_verified:
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message="invalid/expired promocode.").return_response_object()
        payment_history = data['summary']
        if not shops_and_product_structure_validation(shops):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message="please provide valid data 1.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valide data 2.").return_response_object()
    #review shops and products availablity and price variations
    is_failed, response_data, total_payment_ = reiview_shops_and_product(shops)
    if is_failed:
        return SuccessResponse(status_code=SUCCESS_RESPONSE_CREATED,
                               message='failed',data=response_data).return_response_object()
    
    #calculate service and delivery fee and compare the results with request data
    delivery_fee_, service_fee_ = get_delivery_and_service_charges(shops, buyer_)
    total_payment_+= service_fee_+delivery_fee_
    total_payment_ = round(total_payment_, 2)
    request_total_payment = round(float(payment_history['total_payment']), 2)
    if not request_total_payment == total_payment_:
        return FailureResponse(status_code=BAD_REQUEST_CODE, 
                               message='payment conflicted.').return_response_object()
    return SuccessResponse(message='payment verfiied.').return_response_object()




#Checkout
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def checkout(request):
    total_payment_ = 0
    discount_by_promocode = 0
    try:#check already placed order
        buyer_ = request.user
        user_profile = UserProfile.objects.get(user=buyer_)
        customer_id = user_profile.strip_customer_key
        #User cannot place order when its order already in pending
        # if Order.objects.filter(buyer=buyer_,  order_status=PENDING).exists() or Order.objects.filter(buyer=buyer_,  order_status=ACCEPTED).exists():
        #     return FailureResponse(status_code=BAD_REQUEST_CODE,
        #                             message='You are unable to place another order on same time.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='invalid user').return_response_object()
    try:
        data = get_request_obj(request)
        data = data['checkout']
        shops = data['shops']
        payment_history = data['summary']
        is_promocode_verified = data['is_promocode_verified']
        promocode = data['promocode']
        if not shops_and_product_structure_validation(shops):
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message="please provide valid data structure.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valide data.").return_response_object()
    
    #setting order delivery options(Self Pickup, Delivery by driver or Schedule order later)
    try:#check delivery method
        delivery_id_ = data['delivery_option_id']
        delivery_type_ = Delivery_Options.objects.get(id=delivery_id_)            
    except:
        schedule_time_ = data['schedule_time']
        # schedule_time_ = "2021-08-04 15:44:25"
        try:
            try:
                schedule_time_ =  dt.datetime.strptime(schedule_time_, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='please provide valid schedule time format.').return_response_object()
            #we need to validate schedule time for later
        except:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='please provide valid delivery data.').return_response_object()
    
    #Setting shipping address
    try: #get buyer default/delivery address
        buyer_shipping_address_ =  User_Addresses.objects.filter(user=buyer_, is_default=True).last()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message='Kindly set your delivery address.').return_response_object()
    
    is_failed, response_data, total_payment_ = reiview_shops_and_product(shops)
    if is_failed:
        return SuccessResponse(message='failed',data=response_data).return_response_object()
    
    #validate promocode
    if is_promocode_verified:
        is_verified, promocode_data = promocode_verification(promocode)
        if not is_verified:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="invalid/expired promocode.").return_response_object()
        else:
            discount_by_promocode = float(promocode_data['discount_in_percentage'])
            
    #validate total payment
    delivery_fee_, service_fee_ = get_delivery_and_service_charges(shops, buyer_)
    total_payment_+=  service_fee_+delivery_fee_
    total_payment_ = round(total_payment_, 2)
    request_total_payment = round(float(payment_history['total_payment']), 2)
    if not request_total_payment == total_payment_:
        return SuccessResponse(status_code=SUCCESS_RESPONSE_CREATED, 
                               message='payment conflicted.',data={"amount":total_payment_}).return_response_object()
    
    #place an order
    try:
        create_order_ = Order.objects.create(buyer=buyer_, service_fee=service_fee_, delivery_fee=delivery_fee_,
                                            total_amount=total_payment_, shipping_address=buyer_shipping_address_,
                                            order_status=DISPUTED)
        try:
            coupon_object = Coupon.objects.get(secret_code=promocode)
            BuyerAppliedCoupon.objects.create(buyer=buyer_, order=create_order_,coupon=coupon_object)
        except Exception as e:
            print(e)
        try:
            create_order_.delivery_type = delivery_type_
            create_order_.save()
        except:
            try:
                Delivery_Scheduling.objects.create(order=create_order_,schedule_time=schedule_time_)
            except Exception as e:
                print(e)
                create_order_.delete()
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='failed to set delivery type.').return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message='unable to place order, try again.').return_response_object()
    
    #save shop order instances
    for shop in shops:
        shop_sub_total = float(shop['shop_sub_total_price'])
        shop_object = Shop.objects.get(id=int(shop['shop_id']))
        create_shop_order_ = ShopOrder.objects.create(order=create_order_, shop=shop_object,
                                                      sub_total_amount=shop_sub_total, order_status=DISPUTED)
        try:
            products = shop['products']
            #iterate all products and propanes of shop
            for product in products:
                product_category = product['category'].upper().strip()
                if product_category == PRODUCT:
                    product_object_ = Shop_Product.objects.get(id=int(product['product_id']))
                    Order_Items.objects.create(product=product_object_, 
                                                product_quantity=int(product['quantity']),order=create_shop_order_)
                elif product_category == PROPANE:
                    propane_state_ = str(product['sub_category']).lower().strip()
                    propane_object_ = Propane.objects.get(id=int(product['product_id']))
                    Order_Items.objects.create(propane=propane_object_,  propane_state = propane_state_,
                                                propane_quantity=int(product['quantity']),order=create_shop_order_)
        except Exception as e:
            print(e)
            create_order_.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                                message='unable to place order').return_response_object()    
    
    #Stripe gateway integration(save card, payment intent)
    try:
        ephemeralKey = stripe.EphemeralKey.create(customer=customer_id, stripe_version='2020-08-27',)
        #meta
        meta_object = {
            "order_id": create_order_.id
        }
        
        total_payment_ = calculate_main_order_amount(create_order_)
        # if is_promocode_verified:
        #     total_payment_ = discount_formula(total_payment_, discount_by_promocode)
        #     print(total_payment_,'__with promocode')
        total_payment_ = int(float(total_payment_)*100)
        payment_intent = stripe.PaymentIntent.create(
            amount=total_payment_,
            currency="usd",
            payment_method_types=["card"],
            customer = customer_id,
            metadata = meta_object,
            capture_method='manual',
        )
        
        try:
            StripeOrderPaymentIntent.objects.create(buyer=buyer_,create_payment_intent_id= payment_intent.id,
                                                    create_payment_intent_client_secret = payment_intent.client_secret,
                                                    order=create_order_, create_ephemeral_key=ephemeralKey.secret)
            pass
        except Exception as e:
            print(e)
            create_order_.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="unable to process payment, try again.").return_response_object()
        
        #response
        data = {
         'payment_intent' : payment_intent.client_secret,
         'customer_id' : customer_id,
         'ephemeral_key' : ephemeralKey.secret,
         "order_id" : create_order_.id
        }
        return SuccessResponse(message="success", data=data).return_response_object()

    except Exception as e:
        create_order_.delete()
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='something went wrong with payment. try agian').return_response_object()


#handle payment success and failed status of checkout.
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def handle_checkout_payment_status(request):
    main_order_status = PENDING
    shop_order_status = PENDING
    try:
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        payement_status = data['is_payment_successed']
        try:
            int(payement_status)
            if int(payement_status) == 1:
                payement_status = True
            elif int(payement_status) == 0:
                payement_status = False
        except Exception as e:
            print(e)
        if not type(payement_status) == type(True):
            print(payement_status)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data type").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="please provide valid data").return_response_object()
    #handle success payament
    if payement_status:
        try:
            try:
                order = Order.objects.get(id=order_id)
                if Delivery_Scheduling.objects.filter(order=order).exists():
                    main_order_status = SCHEDULED
                    shop_order_status = SCHEDULED
                order.is_payment_procced=False
                order.order_status = main_order_status
                order.save()
                ShopOrder.objects.filter(order__id=order_id).update(order_status=shop_order_status)
                # set_firebase_order_node(create_order_)
                if not main_order_status == SCHEDULED:
                    assign_drivers_to_order(order)
                    message_title = str("New Order #"+str(order.id))
                    message_body = str("You have new order in status "+str(order.order_status))
                    set_firebase_order_tracking_info(order)
                    set_firebase_order_node(order, main_order_status)
                    notify_users_on_order_updates(order, message_title, message_body, users_roles=[SELLER_ROLE])
                return SuccessResponse(message="payment success").return_response_object()
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE, 
                                    message="invalid order").return_response_object()
        except Exception as e:
            print(e)
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message="payment failed").return_response_object()
    #update the order payment status is failed when payment is cancelled or failed
    elif not payement_status:    
        try:
            Order.objects.filter(id=order_id).update(is_payment_procced=False,order_status=DISPUTED)
            ShopOrder.objects.filter(order__id=order_id).update(order_status=DISPUTED)
            AssignOrderToDriverForAcceptence.objects.filter(order__id=order_id).delete()
            return SuccessResponse(message="payment cancelled.").return_response_object()
        except Exception as e:
            Order.objects.filter(id=order_id).delete()
            print(e)
            return FailureResponse(status_code=status.HTTP_304_NOT_MODIFIED,
                                    message="please try again.").return_response_object()
    

#re-checkout the the disputed order
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def recheckout_disputed_order(request):
    try:
        buyer = request.user
        data = get_request_obj(request)
        order_id = int(data['order_id'])
        order = Order.objects.get(id=order_id)
        user_profile_object = UserProfile.objects.get(user=buyer)
        customer_id = user_profile_object.strip_customer_key
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data').return_response_object()
    try:
        ephemeralKey = stripe.EphemeralKey.create(customer=customer_id, stripe_version='2020-08-27',)
        #meta
        meta_object = {
            "order_id": order_id
        }
        total_payment_ = calculate_main_order_amount(order)
        total_payment_ = int(float(total_payment_)*100)
        payment_intent = stripe.PaymentIntent.create(
            amount=total_payment_,
            currency="usd",
            payment_method_types=["card"],
            customer = customer_id,
            metadata = meta_object,
            capture_method='manual',
        )
        try:
            payment_intent_object = StripeOrderPaymentIntent.objects.get(order__id=order_id)
            payment_intent_object.create_payment_intent_client_secret = payment_intent.client_secret
            payment_intent_object.create_ephemeral_key = ephemeralKey.secret
            payment_intent_object.save()
            pass
        except Exception as e:
            print(e)
            order.delete()
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                    message="unable to process payment, try again.").return_response_object()
        #response
        data = {
         'payment_intent' : payment_intent.client_secret,
         'customer_id' : customer_id,
         'ephemeral_key' : ephemeralKey.secret,
         "order_id" : order_id
        }
        return SuccessResponse(
            data=data,
            message="success.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unexpected error.').return_response_object()
        

#verify promocode
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, authentication_level=[BUYER_ROLE])
def verify_promocode(request):
    try:
        data = get_request_obj(request)
        promocode = data['promocode']
        is_verified, promocode_data = promocode_verification(promocode)
        if is_verified:
            return SuccessResponse(data=promocode_data).return_response_object()
        else:
            return FailureResponse(status_code=BAD_REQUEST_CODE,
                                   message="invalid/expired promocode.").return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='please provide valid data.').return_response_object()