# Generated by Django 3.0.4 on 2021-03-29 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_auto_20210329_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_product',
            name='vendor',
            field=models.ForeignKey(db_column='vendor', on_delete=django.db.models.deletion.DO_NOTHING, to='seller.Vendor'),
        ),
    ]
