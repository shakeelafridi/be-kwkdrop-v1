# Generated by Django 3.1 on 2021-09-24 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0044_auto_20210924_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccountdetails',
            name='is_bank_account_verified',
            field=models.BooleanField(default=False),
        ),
    ]