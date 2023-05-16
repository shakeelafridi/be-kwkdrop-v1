# Generated by Django 3.1 on 2021-06-04 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0021_userprofile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_email_verified',
            field=models.BooleanField(db_column='is_email_verified', default=False),
        ),
    ]