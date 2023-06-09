# Generated by Django 3.1 on 2021-08-31 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0048_auto_20210831_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='order_status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('completed', 'COMPLETED'), ('cancelled', 'CANCELLED')], default='ACCEPTED', max_length=20),
        ),
    ]
