# Generated by Django 2.2.1 on 2019-06-07 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_connection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='following',
            new_name='followings',
        ),
    ]
