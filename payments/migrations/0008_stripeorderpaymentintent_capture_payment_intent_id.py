# Generated by Django 3.1 on 2021-09-07 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20210907_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeorderpaymentintent',
            name='capture_payment_intent_id',
            field=models.TextField(default=''),
        ),
    ]
