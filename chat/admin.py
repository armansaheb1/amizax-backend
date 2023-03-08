from django.contrib import admin
from .models import ChatSession , ChatSessionMessage
# Register your models here.

admin.site.register(ChatSession)
admin.site.register(ChatSessionMessage)