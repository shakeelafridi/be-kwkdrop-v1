# Generated by Django 3.1 on 2021-06-17 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0025_auto_20210615_0658'),
        ('seller', '0018_auto_20210610_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('sub_total_amount', models.FloatField()),
                ('grand_total_amount', models.FloatField()),
                ('service_fee', models.FloatField()),
                ('delivery_fee', models.FloatField()),
                ('is_driver_accepted', models.BooleanField(default=False)),
                ('is_shop_accepted', models.BooleanField(default=False)),
                ('shipping_address', models.TextField()),
                ('shop_address', models.TextField()),
                ('order_status', models.CharField(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('completed', 'COMPLETED'), ('cancelled', 'CANCELLED')], default='', max_length=10)),
                ('updated_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authModule.userprofile')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authModule.driver')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authModule.shop')),
            ],
        ),
    ]