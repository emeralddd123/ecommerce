# Generated by Django 4.1.3 on 2022-12-06 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_balance_balance_alter_order_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
