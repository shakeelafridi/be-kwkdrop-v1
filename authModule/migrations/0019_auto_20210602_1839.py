# Generated by Django 3.1 on 2021-06-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0018_auto_20210602_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='license_exp_date',
            field=models.DateField(blank=True, db_column='license_exp_date', null=True),
        ),
    ]
