# Generated by Django 3.1 on 2021-09-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_stripeorderpaymentintent_capture_payment_intent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeorderpaymentintent',
            name='create_ephemeral_key',
            field=models.TextField(default=''),
        ),
    ]
