# Generated by Django 3.1 on 2021-09-02 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0053_auto_20210902_0619'),
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverEarning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.order')),
            ],
        ),
        migrations.DeleteModel(
            name='DriverTip',
        ),
    ]
