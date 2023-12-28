# Generated by Django 5.0 on 2023-12-21 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_date_modified_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to='mediafiles/users/cover_pics'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='mediafiles/users/profile_pics'),
        ),
    ]