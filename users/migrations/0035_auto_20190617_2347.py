# Generated by Django 2.2.1 on 2019-06-18 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20190617_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='following',
            field=models.ManyToManyField(related_name='my_followers', to='users.Profile'),
        ),
    ]
