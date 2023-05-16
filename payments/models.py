from seller.models import Order, ShopOrder
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StripeCustomerCardConfiguration(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_card_id = models.TextField(default='')


class StripeOrderPaymentIntent(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    create_payment_intent_id = models.TextField(default='')
    create_payment_intent_client_secret = models.TextField(default='')
    create_ephemeral_key = models.TextField(default='')
    capture_payment_intent_id = models.TextField(default='')
    cancel_payment_intent_id = models.TextField(default='')
    charge_payment_intent_id = models.TextField(default='')
    refund_payment_intent_id = models.TextField(default='')