#get total amount of order
from buyer.models import BuyerAppliedCoupon
from django.db.models.expressions import F
from buyer.buyer_reusable_resources import get_data_in_list
from seller.models import Order_Items, ShopOrder


#calculate main order amount
def calculate_main_order_amount(order):
    #get products from from ordered item
    total_amount = 0.0
    delivery_charges = float(order.delivery_fee)
    service_fee = float(order.service_fee)
    order_item_objects = Order_Items.objects.filter(order__order=order) #ShopOrder > Main Order
    for item in order_item_objects:
        if item.product is not None:
            if item.product.sale_price == 0:
                total_amount+=(int(item.product_quantity)*item.product.price)
            elif item.product.sale_price > 0:
                total_amount+=(int(item.product_quantity)*item.product.sale_price)
        elif item.propane is not None:
            total_amount+=(int(item.propane_quantity)*item.propane.price)
    grand_total = float(total_amount+service_fee+delivery_charges)
    try:
        applied_coupon = BuyerAppliedCoupon.objects.get(order=order)
        discount = float(applied_coupon.coupon.discount_in_percentage)
        grand_total = discount_formula(grand_total, discount)
    except Exception as e:
        print(e)
    return round(float(grand_total), 2)

#calculate penalty when cancel order
def calculate_penalty(order):
    delivery_charges = float(order.delivery_fee)
    service_fee = float(order.service_fee)
    total_amount = float(delivery_charges+service_fee)
    return total_amount

#calculate amount of each shop in main order
def calculate_shop_order_amount(shop_order):
    total_amount = 0.0
    order_item_objects = Order_Items.objects.filter(order=shop_order) #ShopOrder
    for item in order_item_objects:
        if item.product is not None:
            if item.product.sale_price == 0:
                total_amount+=(int(item.product_quantity)*item.product.price)
            elif item.product.sale_price > 0:
                total_amount+=(int(item.product_quantity)*item.product.sale_price)
        elif item.propane is not None:
            total_amount+=(int(item.propane_quantity)*item.propane.price)
    return float(total_amount)

#promocode discount formula
def discount_formula(total_amount, discount):
    total_amount = float(total_amount - ((total_amount * discount)/100))
    return total_amount