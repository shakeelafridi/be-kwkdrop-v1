# Generated by Django 3.1 on 2021-06-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0016_propane_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propane',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]