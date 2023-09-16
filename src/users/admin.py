from sqladmin import ModelView

from .models import User

class UserAdmin(ModelView, model=User):
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'
    column_list = [User.id, User.username, User.email, User.avatar, User.is_active, User.is_superuser]
    column_details_exclude_list = [User.password, User.access_token]
    can_export = False
