from enum import Enum

from django.core.validators import RegexValidator
from django.db import models


class AbstractTemplate(models.Model):
    slug = models.SlugField(
        verbose_name='Тип шаблона',
        primary_key=True,
        help_text='Слаг, который будет идентифицировать конкретный шаблон'
    )
    description = models.CharField(
        verbose_name='Описание шаблона',
        blank=False,
        max_length=250
    )

    class Meta:
        abstract = True


class PersonalizedTemplate(AbstractTemplate):
    template = models.TextField(
        verbose_name='Текст шаблона',
        validators=[RegexValidator(
            regex='^<.*>.*</.*>$|^[^<>/]+$',
            message='Необходимо ввести валидный html текст или просто строку без тэгов'
        )],
        help_text='Текст персонализированного шаблона. Возможно использовать внутри следующие вставки: {{ username '
                  '}}, {{ filmname }} и '
                  'другие '
    )

    class Meta:
        verbose_name = 'Персонализированный шаблон'
        verbose_name_plural = 'Персонализированные шаблоны'


class CommonTemplate(AbstractTemplate):
    template = models.TextField(
        verbose_name='Текст шаблона',
        validators=[RegexValidator(
            regex='^<.*>.*</.*>$|^[^<>/]+$',
            message='Необходимо ввести валидный html текст или просто строку без тэгов'
        )],
        help_text='Текст шаблона общей рассылки. html страница с общей информацией или просто текст.'
    )

    class Meta:
        verbose_name = 'Общий шаблон'
        verbose_name_plural = 'Общие шаблоны'


class MessageTypes(Enum):
    AUTH = 'AUTH'
    MASS_DELIVERY = 'MASS'
    UGC = 'UGC'
