from django.contrib import admin

# Register your models here.
from .models import create_company,chat_log,template_config,MyLongProcess,webchat_widget

admin.site.register(create_company)
admin.site.register(chat_log)
admin.site.register(template_config)
admin.site.register(MyLongProcess)
admin.site.register(webchat_widget)