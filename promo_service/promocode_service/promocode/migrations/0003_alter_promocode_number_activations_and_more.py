# Generated by Django 4.1.7 on 2023-03-30 19:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("promocode", "0002_alter_promocode_number_activations_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="promocode",
            name="number_activations",
            field=models.PositiveIntegerField(
                default=0, editable=False, verbose_name="number activations"
            ),
        ),
        migrations.AlterField(
            model_name="promocode",
            name="personal_user_id",
            field=models.UUIDField(
                blank=True, null=True, verbose_name="personal user id"
            ),
        ),
        migrations.AlterField(
            model_name="promocodetype",
            name="description",
            field=models.TextField(verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="promocodetype",
            name="discount",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="discount",
            ),
        ),
        migrations.AlterField(
            model_name="promocodetype",
            name="duration",
            field=models.PositiveIntegerField(verbose_name="duration"),
        ),
        migrations.AlterField(
            model_name="promocodetype",
            name="max_number_activation",
            field=models.PositiveIntegerField(
                default=0, verbose_name="max number activation"
            ),
        ),
        migrations.AlterField(
            model_name="promocodetype",
            name="type_id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="type id",
            ),
        ),
        migrations.AlterField(
            model_name="promocodeuserhistory",
            name="activated_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="activated at"),
        ),
        migrations.AlterField(
            model_name="promocodeuserhistory",
            name="expire_at",
            field=models.DateTimeField(verbose_name="expire at"),
        ),
        migrations.AlterField(
            model_name="promocodeuserhistory",
            name="promo_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="promocode.promocode",
                verbose_name="promo id",
            ),
        ),
        migrations.AlterField(
            model_name="promocodeuserhistory",
            name="user_id",
            field=models.UUIDField(verbose_name="user id"),
        ),
    ]