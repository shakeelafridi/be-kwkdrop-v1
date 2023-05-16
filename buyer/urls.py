from buyer.checkout import checkout, handle_checkout_payment_status, recheckout_disputed_order, validate_checkout, verify_promocode
from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    path('buyer-desktop/', desktop),
    path('search-products-and-shops/', search_products_and_shops),
    path('get-all-shops/', get_shops_for_buyer),
    path('get-products-for-buyer/',get_products_for_buyer),
    path('product-details/',product_details),
    # cart is operated on frontend
    # path('buyer-add-to-cart/',buyer_add_to_cart),
    path('get-products-from-cart/',get_data_from_cart),
    # path('qutick-edit-to-cart/',quick_edit_to_cart),
    # path('delete-item-from-cart/',delete_item_from_cart),
    path('get-profile/',get_profile),
    path('propane-suggested-list/', propane_suggested_list),
    path('buyer-address-manipulation/', buyer_address_manipulation),
    # path('promo-code/', promo_code),
    path('delivery-addresses-manipulations/', delivery_addresses_manipulations),
    path('delivery-options/',delivery_options),
    path('validate-checkout/',validate_checkout),
    path('checkout/',checkout),
    path('handle-checkout-payment-status/',handle_checkout_payment_status),
    path('recheckout-disputed-order/', recheckout_disputed_order),
    path('get-order-details/',get_order_details),
    path('get-orders-history/', get_orders_history),
    path('get-delivery-and-service-fee/', get_delivery_and_service_fee),
    path('review-product/',review_product),
    path('assign-driver/',assign_driver),
    path('tip-and-review-driver/',tip_and_review_driver),
    path('get-products-for-review/', get_products_for_review),
    path('suggest-items-during-order-modification/',suggest_items_during_order_modification),
    path('add-new-item-in-order/',add_new_item_in_order),
    path('verify-promocode/', verify_promocode),
    path('order-tracking/', order_tracking),
    
    #testing purposes only
    # path('execute-randome-query/', execute_randome_query)

    #get order serializer
    # path('get-order-list/', get_order),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
