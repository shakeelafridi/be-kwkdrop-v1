# Generated by Django 3.1 on 2021-08-20 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0038_order_is_payment_procced'),
        ('payments', '0003_stripecustomerintent'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecustomerintent',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seller.order'),
        ),
    ]
