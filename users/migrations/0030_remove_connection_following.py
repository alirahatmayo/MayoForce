# Generated by Django 2.2.1 on 2019-06-18 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_auto_20190617_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='following',
        ),
    ]
