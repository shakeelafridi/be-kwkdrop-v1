# Generated by Django 3.1 on 2021-06-10 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0015_propane_propane_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propane_Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('propane_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.propane_company')),
            ],
        ),
    ]
