# Generated by Django 3.1 on 2021-08-31 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0046_orderdoorstepdelivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='driver_accepted_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
