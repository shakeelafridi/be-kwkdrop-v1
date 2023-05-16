# Generated by Django 3.1 on 2021-08-31 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0047_order_driver_accepted_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_shops_accepted',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='order_status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('completed', 'COMPLETED'), ('cancelled', 'CANCELLED')], default='ACCEPTED', max_length=10),
        ),
    ]