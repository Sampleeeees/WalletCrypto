from sqladmin import ModelView

from .models import Order


class OrderAdmin(ModelView, model=Order):
    name = 'Order'
    name_plural = 'Orders'
    icon = 'fa fa-shopping-cart'
    column_list = [Order.id, Order.status, Order.product_id, Order.transaction_id, Order.date_send]
    column_details_exclude_list = [Order.product, Order.transaction]
    can_export = False