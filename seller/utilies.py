#_________________________________if cancel order_____________________________
'''        
        if role_ == BUYER_ROLE and order_status_ == CANCELLED:
            try:
                #if buyer cancel the order when its get prepared by shop. there will be penalty on buyer
                #the penalty charges will be equal to delivery charges.
                stripe_intent=StripeCustomerIntent.objects.get(order=get_order)
                payment_intent_id = stripe_intent.payment_intent
                if get_order.order_status == PREPARED and role_ == BUYER_ROLE and order_status_==CANCELLED:
                    #create a logic to penalty on buyer
                    pass
                else:
                    cancel_payment_intent = stripe.PaymentIntent.cancel(
                        payment_intent_id,
                        )
                    stripe_intent.cancel_payment_intent = cancel_payment_intent
                    stripe_intent.save()
                get_order.order_status=order_status_
                get_order.cancelled_by = BUYER_ROLE
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="unexpected error, try again.").return_response_object()
        elif role_ == SELLER_ROLE:
            try:
                if not get_order.shop.seller.user == user_:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="invalid order.").return_response_object()
                get_order.order_status=order_status_
                get_order.cancelled_by = SELLER_ROLE
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="unexpected error, try again.").return_response_object()
        elif role_ == DRIVER_ROLE:
            try:
                if not get_order.driver.user== user_:
                    return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="invalid order.").return_response_object()
                get_order.order_status=order_status_
            except Exception as e:
                print(e)
                return FailureResponse(status_code=BAD_REQUEST_CODE,
                                        message="unexpected error, try again.").return_response_object()
                                        
'''