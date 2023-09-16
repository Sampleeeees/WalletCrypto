from sqladmin import ModelView

from .models import Product


class ProductAdmin(ModelView, model=Product):
    name = 'Product'
    name_plural = 'Products'
    icon = 'fa fa-tags'
    column_list = [Product.id, Product.name, Product.image, Product.price, Product.wallet_id]
    column_details_exclude_list = [Product.wallet]
    can_export = False