# Generated by Django 3.1 on 2021-06-10 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0014_auto_20210609_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='propane',
            name='propane_category',
            field=models.CharField(choices=[('new', 'NEW'), ('exchange', 'EXCHANGE'), ('upgrade', 'UPGRADE'), ('deposite', 'DEPOSITE')], default='', max_length=8),
        ),
    ]
