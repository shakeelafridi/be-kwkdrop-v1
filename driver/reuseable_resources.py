#update driver latest lat lng on server from firebase

from authModule.models import DriverRadiusSettings
from re import I
from kwk.settings import FIREBASE_DATABASE
from seller.models import Order, ShopOrder
import json
from utilities.constants import progress_order_list


def update_driver_lat_lng(order_id):
    try:
        lat = None
        lng = None
        shop_order_object = ShopOrder.objects.filter(order__id=order_id).last()
        driver_id = shop_order_object.driver.id
        latest_order = ShopOrder.objects.filter(driver__id=driver_id, order_status__in=progress_order_list).latest('created_at')
        order_id = latest_order.order.id
        data = FIREBASE_DATABASE.child("order_tracking").child(order_id).child('driver_address').get().val()
        for key, val in data.items():
            if str(key).lower() == "lat":
                lat = val
            if str(key).lower() == "lng":
                lng = val
        DriverRadiusSettings.objects.filter(driver__id=driver_id).update(lat=lat,lng=lng)
    except Exception as e:
        print(e)