# Generated by Django 3.1 on 2021-08-25 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20210825_1836'),
        ('seller', '0039_auto_20210825_1836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]