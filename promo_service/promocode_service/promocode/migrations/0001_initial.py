# Generated by Django 4.1.7 on 2023-04-13 18:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import promocode.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Promocode",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "promo_value",
                    models.CharField(
                        default=promocode.models.get_promo_code,
                        max_length=20,
                        validators=[django.core.validators.MinLengthValidator(8)],
                        verbose_name="promo value",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                ("is_valid", models.BooleanField(verbose_name="is valid")),
                (
                    "personal_user_id",
                    models.UUIDField(
                        blank=True, null=True, verbose_name="personal user id"
                    ),
                ),
                ("activate_until", models.DateTimeField(verbose_name="activate until")),
            ],
            options={
                "verbose_name": "promocode",
                "verbose_name_plural": "promocodes",
                "db_table": "promocode",
            },
        ),
        migrations.CreateModel(
            name="PromocodeType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="type id",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="discount",
                    ),
                ),
                ("duration", models.PositiveIntegerField(verbose_name="duration")),
                (
                    "max_number_activation",
                    models.PositiveIntegerField(
                        default=0, verbose_name="max number activation"
                    ),
                ),
            ],
            options={
                "verbose_name": "promocode type",
                "verbose_name_plural": "promocode type",
                "db_table": "promocode_type",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="type id",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "users_api_endpoint",
                    models.URLField(verbose_name="users api endpoint"),
                ),
                (
                    "notify_api_endpoint",
                    models.URLField(verbose_name="notify api endpoint"),
                ),
                (
                    "is_complete",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="is complete"
                    ),
                ),
                (
                    "promocode_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="promocode.promocodetype",
                        verbose_name="type of promocode",
                    ),
                ),
            ],
            options={
                "verbose_name": "task",
                "verbose_name_plural": "tasks",
                "db_table": "task",
            },
        ),
        migrations.CreateModel(
            name="PromocodeUserHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.UUIDField(verbose_name="user id")),
                (
                    "activated_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="activated at"
                    ),
                ),
                (
                    "promocode_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="promocode.promocode",
                        verbose_name="promo id",
                    ),
                ),
            ],
            options={
                "verbose_name": "promocode history",
                "verbose_name_plural": "promocode history",
                "db_table": "promocode_user_history",
            },
        ),
        migrations.AddField(
            model_name="promocode",
            name="promocode_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="promocode.promocodetype",
                verbose_name="type of promocode",
            ),
        ),
        migrations.AddConstraint(
            model_name="promocodeuserhistory",
            constraint=models.UniqueConstraint(
                fields=("promocode_id", "user_id"), name="unique pair promocode-user"
            ),
        ),
    ]
