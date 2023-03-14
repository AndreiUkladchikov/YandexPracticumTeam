from django.contrib import admin

from admin_panel.models import PersonalizedTemplate, CommonTemplate


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
        for template in queryset:
            pass
            # send_message(template)
