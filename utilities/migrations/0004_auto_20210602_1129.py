# Generated by Django 3.1 on 2021-06-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0003_usstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_product_barcode_scanner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', null=True),
        ),
        migrations.AddField(
            model_name='usstate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', null=True),
        ),
    ]
