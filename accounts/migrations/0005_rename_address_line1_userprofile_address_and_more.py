# Generated by Django 5.0 on 2024-02-08 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_phone_no_alter_userprofile_cover_pic_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_line1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line2',
        ),
    ]