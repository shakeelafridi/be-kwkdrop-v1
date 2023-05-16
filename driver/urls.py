from django.urls import path
from django.conf.urls.static import static
from kwk.settings import MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    path('set_driver_radius/', set_driver_radius),
    path('get-states-and-vehicle-type/', get_states_and_vehicle_type),
    path('driver-desktop-and-status-ru/', driver_desktop_and_status_ru),
    path('get-orders-list-for-driver/',get_orders_list_for_driver),
    path('accpet-or-reject-order-by-driver/',accpet_or_reject_order_by_driver),
    path('get-order-details-for-driver/',get_order_details_for_driver),
    path('order-doop-step-delivered/',order_doop_step_delivered),
    path('get-driver-earning/',get_driver_earning),
    path('get-driver-order-history/',get_driver_order_history),
    path('driver-checker-verification-status/',driver_checker_verification_status),
    # path('insert-US-states/', insert_US_states),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
