# Generated by Django 4.1.3 on 2022-12-04 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='nan', upload_to=''),
            preserve_default=False,
        ),
    ]
