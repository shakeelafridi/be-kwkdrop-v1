# Generated by Django 3.1 on 2021-06-25 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0030_auto_20210624_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_addresses',
            name='is_default',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user_addresses',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
