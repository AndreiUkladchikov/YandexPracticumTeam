# Generated by Django 4.1.7 on 2023-04-03 20:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        (
            "promocode",
            "0004_remove_promocodeuserhistory_unique pair promocode-user_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="promocodeuserhistory",
            name="expire_at",
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
                ("api_endpoint", models.URLField(verbose_name="api endpoint")),
                (
                    "is_complete",
                    models.BooleanField(default=False, verbose_name="is complete"),
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
    ]