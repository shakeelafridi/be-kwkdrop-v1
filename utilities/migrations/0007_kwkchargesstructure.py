# Generated by Django 3.1 on 2021-08-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0006_kwkusecase_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='kwkChargesStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_charges_in_percentage', models.FloatField()),
                ('delivery_charges_per_kilometer', models.FloatField()),
            ],
        ),
    ]
