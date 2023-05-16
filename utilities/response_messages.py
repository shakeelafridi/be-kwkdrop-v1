#common messages for all roles(seller, buyer, driver)
INVALID_ROLE = "invalid role."
INVALID_USER = "invalid user."
INVALID_SHOP = 'invalid shop.'
INVALID_SELLER = 'invaid seller.'
UNFILLED_ADDRESS = 'kindly set address.'
INVALID_DATA_TYPE = 'invalid data type.'

#seller module messags
INVALID_SELLER_FOR_REQUESTED_SHOP = "shop does not belong to the requested shop."
INVALID_VENDOR_FOR_REQUESTED_SHOP = "vendor does not belong to the requested shop."
INVALID_PRODUCT_FOR_REQUESTED_SHOP = 'product does not belongs to the requested shop.'
INVALID_OPTION_FOR_REQUESTED_SHOP = 'option name does not belongs to the shop.'
SELLER_NOT_FOUND = "seller does not exists."
SELLER_NOT_ACTIVE = 'seller role is not active.'
SKU_NOT_FOUND = 'product sku not found.'
SALE_PRICE_GREATER_CONFLICT = 'sale price should less than actual price.'
BARCODE_ALREADY_EXISTS = 'product barcode already registered.'
SKU_ALREADY_EXISTS = 'product sku aleady registered.'
CSV_READING_FAILED = "unable to read csv file or invalid csv format."
CSV_PRODUCTS_READING_FAILED = 'invalid data format for some products.'
PRODUCT_NOT_FOUND = 'product not found.'
PROPANE_NOT_FOUND = 'propane not found.'
OPTIONS_NOT_FOUND = 'options not found.'
INVALID_SHOP_HOURS = 'shop hours are not valid.'
INVALID_QUANTITY_AMOUNT = 'quantity should be greater than zero.'
INVALID_PROPANE_COMPANY = 'invalid propane company.'
COMPANY_NOT_FOUND = 'company not found.'
PROPANE_PRICE_NOT_FOUND = 'unable to get propane price.'

#order response messages
INVALID_ORDER = 'invalid order.'
ORDER_NOT_FOUND = 'order not found.'
INVALID_ORDER_STATUS = 'invalid orde status.'
ORDER_IS_DISPUTED = 'order is disputed.'
ALREADY_COMPLETED = 'order is already completed.'
FAILED_COMPLETION = 'unable to complete order, try again.'
ALREADY_CANCELLED = 'order is already cancelled.'
ALREADY_DELIVERED = 'order is already delivered.'
CANCELLATION_TIME_EXPIRED = 'unable to cancel the order, time expired.'
FAILED_CANCELLATION = 'cancellation failed, try again.'
ORDER_STATUS_UPDATED = 'order status updated.'
INVALID_ORDER_ITEM = 'invalid ordered item.'

#incomplete request messages
UNFILLED_DATA = "please fill all the data."
PROVIDE_VALID_DATA = "please provide valid data."
SOMETHING_WENT_WRONG = 'Something went wrong.'

#CRUD messages
SUCCESS_CREATED = 'records successfully created.'
SUCCESS_UPDATED = 'records successfully updated.'
SUCCESS_DELETED = 'records successfully deleted.'
FAILED_CREATED = 'failed to create records.'
FAILED_DELETED = 'deletion failed.'
