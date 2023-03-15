from django.contrib import admin

from admin_panel.config import settings
from admin_panel.models import PersonalizedTemplate, CommonTemplate
from admin_panel.clients import HttpClient, RabbitClient


@admin.register(PersonalizedTemplate)
class PersonalizedTemplateAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    list_display = ('slug',)


@admin.register(CommonTemplate)
class CommonTemplateAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    list_display = ('slug',)
    actions = ('send_template', )

    @admin.action(description='Отправить шаблон всем пользователям')
    def send_template(self, request, queryset):
        http_client = HttpClient()
        rabbit_client = RabbitClient()
        list_of_ids = http_client.get_all_user_ids(
            url=settings.all_users_auth_url
        )
        for template in queryset:
            for user_id in list_of_ids:
                rabbit_client.send_message({
                    'type': template.slug,
                    'subject': 'Сообщение для пользователей',
                    'template': template.template,
                    'user_id': user_id,
                })
