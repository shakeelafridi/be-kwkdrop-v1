# Generated by Django 3.1 on 2021-07-02 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0028_auto_20210702_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignordertodriverforacceptence',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.order'),
        ),
    ]