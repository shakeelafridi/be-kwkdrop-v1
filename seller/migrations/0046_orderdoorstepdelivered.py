# Generated by Django 3.1 on 2021-08-30 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0045_assignordertodriverforacceptence_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDoorStepDelivered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.JSONField(null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.order')),
            ],
        ),
    ]
