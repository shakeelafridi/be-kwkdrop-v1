# Generated by Django 3.1 on 2021-09-02 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0041_shop_image'),
        ('driver', '0002_auto_20210902_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverearning',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authModule.driver'),
        ),
        migrations.AddField(
            model_name='driverearning',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]