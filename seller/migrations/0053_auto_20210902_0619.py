# Generated by Django 3.1 on 2021-09-02 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0052_order_items_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='item_status',
            field=models.CharField(default='to-do', max_length=20),
        ),
    ]