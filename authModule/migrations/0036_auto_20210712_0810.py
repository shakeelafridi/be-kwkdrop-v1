# Generated by Django 3.1 on 2021-07-12 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModule', '0035_userprofile_email_verification_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(db_column='phone_number', default='', max_length=20),
        ),
    ]