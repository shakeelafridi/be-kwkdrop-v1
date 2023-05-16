# Generated by Django 3.1 on 2021-06-30 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0025_auto_20210630_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery_Scheduling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('complete_order', models.BooleanField(default=False)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.order')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.delivery_options'),
        ),
    ]