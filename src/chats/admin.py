from sqladmin import ModelView

from .models import Message

class MessageAdmin(ModelView, model=Message):
    """Admin модель для керування даними"""
    name = 'Message'
    name_plural = 'Messages'
    icon = 'fa fa-comments'
    column_list = [Message.id, Message.content, Message.image, Message.date_send, Message.user_id]
    can_export = False