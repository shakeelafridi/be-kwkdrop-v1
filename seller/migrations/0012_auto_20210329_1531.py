# Generated by Django 3.0.4 on 2021-03-29 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0011_auto_20210329_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_product_category',
            name='shop_product',
            field=models.ForeignKey(db_column='shop_product', null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.Shop_Product'),
        ),
    ]
