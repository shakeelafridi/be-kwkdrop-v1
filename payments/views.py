from authModule.models import UserProfile
from utilities.reuseableResources import get_request_obj
from utilities.ResponseHandler import FailureResponse, SuccessResponse
from utilities.RequestHandler import DecoratorHandler
from utilities.constants import BAD_REQUEST_CODE, BUYER_ROLE, DRIVER_ROLE, SELLER_ROLE
from kwk.settings import *
import stripe
from utilities.constants import *
decorator_ = DecoratorHandler()
stripe.api_key = STRIP_SECRET_KEY

# Create your views here.

def calculate_main_order_amount(items):
    
    # Replace this constant with a calculation of the order's amount

    # Calculate the order total on the server to prevent

    # people from directly manipulating the amount on the client

    return 500 #cents

#procced checkout payments
@decorator_.rest_api_call(allowed_method_list=['POST'], is_authenticated=True, 
                          authentication_level=[BUYER_ROLE, SELLER_ROLE, DRIVER_ROLE])
def procced_payment(request):
    try:
        data = get_request_obj(request)
        amount_ = int(float(data['amount'])*100)
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        customer_id = user_profile.strip_customer_key
        print(customer_id)
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unable to get user').return_response_object()
    
    try:
        product_list = []
        # customer = stripe.Customer.create(
        #     description="My First Test Customer (created for API docs)",
        #     email = "email@email.com",
        #     name = "name",
        # )
        # print('customer_id: ', customer['id'])
        ephemeralKey = stripe.EphemeralKey.create(
            customer=customer_id,
            stripe_version='2020-08-27',
        )
        
        product_list.append('1')
        product_list.append('1')
        
        paymentIntent = stripe.PaymentIntent.create(
            amount=amount_,
            currency="usd",
            payment_method_types=["card"],
            customer = customer_id,
            metadata = product_list,
        )
        
        stripe.Customer.create_source(
            customer_id,
            source="tok_amex",
        )
        
        data ={
         'payment_intent' : paymentIntent.client_secret,
         'customer_id' : customer_id,
         'ephemeral_key' : ephemeralKey.secret,
        }
        
        return SuccessResponse(message="success", data=data).return_response_object()
    except Exception as e:
        print(e)
        return FailureResponse(status_code=BAD_REQUEST_CODE,
                                message='unexpected error, try agian').return_response_object()
    
    
def get_stripe_cards(request):
    cust_id = "cus_K0uq7yHmUSnVMI"
    cards = stripe.Customer.list_sources(
        cust_id,
        object="card",
        limit=3,
        )
    return SuccessResponse(data=cards).return_response_object()

    # cust = stripe.Customer.retrieve(cust)
    
    # stripe.Customer.create_source(
    #     cust,
    #     source="tok_amex",
    # )
    
    # stripe.Customer.retrieve_source(
    #     "cus_AJ6mqoWgCYI0wY",
    #     "card_1JMprt2eZvKYlo2CApVouG65",
    # )
    


# def user_payment_sheet(request):
#     # Use an existing Customer ID if this is a returning customer
#     try:
#         customer = stripe.Customer.create()
#         ephemeralKey = stripe.EphemeralKey.create(
#             customer=customer['id'],
#             stripe_version='2020-08-27',
#         )
#         paymentIntent = stripe.PaymentIntent.create(
#             amount=700,
#             currency='usd',
#             customer=customer['id']
#         )
        
#         data = {} 
#         data['payment_intent'] = paymentIntent.client_secret
#         data['ephemeral_key'] = ephemeralKey.secret
#         data['customer_id'] = customer.id
#         return HttpResponse(json.dumps(data), content_type="application/json")
#     except Exception as e:
#         return HttpResponse(str(e))
    
# def get_customer(request):
#     cust_id = 'cus_Jqnsda9BKlH9zl'
#     cust_ = stripe.Customer.retrieve(cust_id) #retrive customer details
#     cust_ = stripe.PaymentIntent.list(limit=3,customer=cust_id) #retrive customer payment intent details
#     cust_ = stripe.Customer.list_sources(
#         cust_id,
#         object="card",
#         limit=3,
#         )
#     return HttpResponse(json.dumps(cust_), content_type="application/json")

# def payment_refund(request):
#     try:
#         refund = stripe.Refund.create(
#             amount=1000,
#             payment_intent='pi_Aabcxyz01aDfoo',
#         )  
#         return HttpResponse(json.dumps(refund), content_type="application/json")
#     except Exception as e:
#         return HttpResponse(str(e))
    
# def payment_cancel(request):
#     try:
#         intent = stripe.PaymentIntent.cancel('pi_32AkjQ5H4Bas2eAolX13')
#         return HttpResponse(json.dumps(intent), content_type="application/json")
#     except Exception as e:
#         return HttpResponse(str(e))
   
