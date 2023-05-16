# Generated by Django 3.0.4 on 2021-03-18 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_Product_Barcode_Scanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.TextField(db_column='barcode', default='')),
                ('title', models.TextField(db_column='title', default='')),
                ('product_img', models.TextField(db_column='product_img', default='')),
                ('category', models.TextField(db_column='category', default='category')),
                ('type', models.TextField(db_column='type', default='')),
            ],
        ),
    ]