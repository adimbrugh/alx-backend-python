from django.contrib import admin

# Register your models here.

from .models import Message, Notification, MessageHistory



admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)