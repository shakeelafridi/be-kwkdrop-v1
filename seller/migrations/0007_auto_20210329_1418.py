# Generated by Django 3.0.4 on 2021-03-29 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0007_auto_20210327_1417'),
        ('seller', '0006_auto_20210329_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='shop',
            field=models.ForeignKey(db_column='shop', null=True, on_delete=django.db.models.deletion.CASCADE, to='authModule.Shop'),
        ),
    ]
