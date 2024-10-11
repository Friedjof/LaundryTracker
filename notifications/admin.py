from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import TelegramBot, TelegramChannel


class TelegramBotResource(resources.ModelResource):
    class Meta:
        model = TelegramBot
        fields = ('identifier', 'name', 'token')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'name', 'token')


class TelegramBotAdmin(ImportExportModelAdmin):
    resource_class = TelegramBotResource
    list_display = ('name', 'formatted_token')

    def formatted_token(self, obj):
        token = obj.token
        if len(token) > 6:
            return f'{token[:5]}{"*" * (len(token) - 10)}{token[-5:]}'
        return token

    formatted_token.short_description = 'Token'


class TelegramChannelResource(resources.ModelResource):
    class Meta:
        model = TelegramChannel
        fields = ('identifier', 'name', 'chat_id', 'telegram_bot', 'building')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'name', 'chat_id', 'telegram_bot', 'building')


class TelegramChannelAdmin(ImportExportModelAdmin):
    resource_class = TelegramChannelResource
    list_display = ('name', 'chat_id', 'telegram_bot', 'building')


# Register your models here.
admin.site.register(TelegramChannel, TelegramChannelAdmin)
admin.site.register(TelegramBot, TelegramBotAdmin)
