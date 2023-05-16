# Generated by Django 3.1 on 2021-06-17 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0019_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(db_column='quantity', default=0)),
                ('propane_quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.order')),
                ('product', models.ForeignKey(db_column='product', null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.shop_product')),
                ('propane', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seller.propane')),
            ],
        ),
    ]
