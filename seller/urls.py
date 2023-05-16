from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    # path('register/', register),
    path('add-vendor/', add_vendor),
    path('show-vendor/', show_vendor),
    path('update-vendor/', update_vendor),
    path('delete-vendor/', delete_vendor),
    path('seller-desktop/', seller_desktop),
    path('get-shop-seller-vendor-product-detais/', get_shop_seller_vendor_product_detais_for_add_product),
    path('add-product-in-shop/', add_Product_in_shop),
    path('get-Product-for-shop/', get_product_for_shop),
    path('delete-Product-in-shop/', delete_product_in_shop),
    path('update-product-in-shop/', update_product_in_shop),
    path('get-products-scanning-barcode/', get_products_scanning_barcode),
    path('quick-edit-shops-product/', quick_edit_shops_product),
    path('add-option-name-for-variant/', add_option_name_for_variant),
    path('get-option-name-for-variant/', get_option_name_for_variant),
    path('delete-option-name-for-variant/', delete_option_name_for_variant),
    path('update-option-name-for-variant/', update_option_name_for_variant),
    path('add-option-value-for-variant/', add_option_value_for_variant),
    path('get-option-value-for-variant/', get_option_value_for_variant),
    path('delete-option-value-for-variant/', delete_option_value_for_variant),
    path('add-products-by-csv/', add_products_by_csv),
    path('add-shop-for-seller/', add_shop_for_seller),
    path('delete-shop-of-seller/', delete_shop_of_seller),
    path('update-shop-of-seller/', update_shop_of_seller),
    path('get-companies', get_companies),
    path('cu-propane/', cu_propane),
    path('propane-inventory/', propane_inventory),
    path('quick-edit-and-delete-propane/', quick_edit_and_delete_propane),
    path('get-seller-order-list/',get_seller_order_list),
    # path('seller-orders-acceptence/',seller_orders_acceptence),
    path('update-order-status/', update_order_status),
    path('get-seller-orders-history/',get_seller_orders_history),
    path('verify-order-items-by-shoper/',verify_order_items_by_shoper),
    path('verify-product-using-barcode-by-shop/', verify_product_using_barcode_by_shop),
    path('confirm-ordered-item-quantity/',confirm_ordered_item_quantity),

    path('upload-images_to_aws/', upload_image_to_aws_and_get_link)
    # path('upload-img/', upload_img),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
