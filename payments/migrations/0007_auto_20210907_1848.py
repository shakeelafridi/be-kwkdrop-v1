# Generated by Django 3.1 on 2021-09-07 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0058_auto_20210906_0904'),
        ('payments', '0006_auto_20210825_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeOrderPaymentIntent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_payment_intent_id', models.TextField(default='')),
                ('cancel_payment_intent_id', models.TextField(default='')),
                ('charge_payment_intent_id', models.TextField(default='')),
                ('refund_payment_intent_id', models.TextField(default='')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seller.order')),
            ],
        ),
        migrations.DeleteModel(
            name='StripeCustomerIntent',
        ),
    ]
