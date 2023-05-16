SUCCESS_RESPONSE_CREATED = 201
SUCCESS_RESPONSE_CODE = 200
METHOD_NOT_ALLOWED = 405
UNAUTHORIZED = 401
PAGE_NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500
BAD_REQUEST_CODE = 400

# User Roles
DRIVER_ROLE = 'DRIVER'
SELLER_ROLE = 'SELLER'
BUYER_ROLE = 'BUYER'

#Driver Roles
TAXI_ROLE = 'TAXI_CAPTAIN'
DELIVERY_ROLE = 'DELIVERY_DRIVER'

#Vehilce Types
VEHICLE_TYPE = 'VEHICLE_TYPE'
BOX_TRUCK = 'BOX_TRUCK'
PICKUP_TRUCK = 'PICKUP_TRUCK'
CAR = 'CAR'
SCOOTER = 'SCOOTER'
BICYCLE = 'BICYCLE'
PEDESTRIAN = 'PEDESTRIAN'

#Tariff
DELIVERY = 'DELIVERY'
SERVICE = 'SERVICE'
PROMO = 'PROMO'

#Deliver Options
DELIVER_NOW = 'DELIVERNOW'
SELF_PICKUP = 'SELFPICKUP'

#Checkr response checks
CLEAR = "clear"

#Order status string
PENDING='pending' #when order placed
ACCEPTED='accepted' #when driver accepted
PICKING = 'picking' #when shop start picking
PREPARED = 'prepared' #when shop prepared
PICKED = 'picked' #when driver picked order
STARTED = 'started' #when driver started order
DELIVERED = 'delivered'#when driver delivered order
COMPLETED='completed' #buyer update status
CANCELLED='cancelled'
DISPUTED='disputed'
PROGRESS = 'progress'
SCHEDULED = 'scheduled'

#progress order status
progress_order_list = [PREPARED, STARTED, PICKED, PICKING, DELIVERED, ACCEPTED, PENDING]
#shop
shop_order_list_status = [ACCEPTED, PROGRESS, COMPLETED]
#driver
driver_order_list_status = [ACCEPTED, PROGRESS, COMPLETED]
#buyer
buyer_order_list_status_for_history = [PENDING, PROGRESS, COMPLETED, CANCELLED, DISPUTED, SCHEDULED]
#get orders accordence list
order_status_list = [PREPARED, COMPLETED, CANCELLED, STARTED, PICKED, PICKING, DELIVERED]
#buyer
buyer_order_list_status = [COMPLETED, CANCELLED, PROGRESS]
#(conditional), unable to cancel order when order's status is in below condition
invalid_order_status_list_for_cancel = [PREPARED,PICKED, STARTED, DELIVERED, COMPLETED]
#conditional when user update the order status
driver_order_status_list = [STARTED,PICKED,DELIVERED,PICKING]
shop_order_status_list = [PREPARED,PICKING]
buyer_order_status_list = [COMPLETED,CANCELLED]
#valid list for adding new item in order(during order)
valid_list_for_new_item_in_order = [PENDING,ACCEPTED,PICKING]

PROPANE = 'PROPANE'
PRODUCT = 'PRODUCT'

#Propane categories
PROPANE_NEW = "new"
PROPANE_EXCHANGE = "exchange"
PROPANE_UPGRADE = "upgrade"
PROPANE_DISPOSE = "dispose"
propane_type_list = [PROPANE_NEW,PROPANE_EXCHANGE,PROPANE_UPGRADE,PROPANE_DISPOSE]

#order item status
TO_DO = 'to-do'
REVIEW = 'review'
DONE = 'done'
order_items_status = [TO_DO,REVIEW,DONE]

DOMAIN_MEDIA_URL = 'http://50.19.158.239:8000'

FORGOT_PASSWORD_KEY_LENGTH = 6
FORGOT_PASSWORD_KEY_VALIDITY_IN_MINUTES = 10

#Default AWS image
DEFAULT_PROFILE_IMAGE = "https://kwkdrop.s3-us-east-2.amazonaws.com/media/1_LK4H69l.jpg"

#Weeks days of shops(validation)
WEEK_DAYS_NAME = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

#Email regular expression(validation)
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

#Social Security Number regular expression(validataion)
snn_regex = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"

#Email verification link(authentication)
EMAIL_VERIFICATION_LINK = 'http://50.19.158.239:8000/api/auth/email-verification/'

#OTP Expirey time
PHONE_NUMBER_OTP_EXPIRY_IN_SECONDS = 60
TWO_MINTS_IN_SECONDS = 120
THREE_MINTS_IN_SECONDS = 180

#Firebase
#Notification sound string
NOTIFICATION_SOUND = 'Snap-of-finger.caf'

#Firebase rules(do not remove)
# {
#   "rules": {
#     ".read": "now < 1627585200000",  // 2021-7-30
#     ".write": "now < 1627585200000",  // 2021-7-30
#   }
# }