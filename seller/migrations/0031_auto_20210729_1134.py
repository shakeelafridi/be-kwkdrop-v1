# Generated by Django 3.1 on 2021-07-29 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0030_auto_20210702_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propane',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='propane_price',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='shop_product_variant',
            name='price',
            field=models.FloatField(db_column='price', default=0),
        ),
        migrations.AlterField(
            model_name='shop_product_variant',
            name='sale_price',
            field=models.FloatField(db_column='sale_price', default=0),
        ),
    ]
