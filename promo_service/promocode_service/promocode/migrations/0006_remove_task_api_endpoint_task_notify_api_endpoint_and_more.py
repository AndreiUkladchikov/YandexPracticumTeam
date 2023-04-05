# Generated by Django 4.1.7 on 2023-04-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promocode", "0005_remove_promocodeuserhistory_expire_at_task"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="api_endpoint",
        ),
        migrations.AddField(
            model_name="task",
            name="notify_api_endpoint",
            field=models.URLField(default="", verbose_name="notify api endpoint"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="users_api_endpoint",
            field=models.URLField(default="", verbose_name="users api endpoint"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="task",
            name="is_complete",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="is complete"
            ),
        ),
    ]