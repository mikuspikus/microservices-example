# Generated by Django 2.2.5 on 2019-11-09 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gatewayuser',
            old_name='identidier',
            new_name='identifier',
        ),
    ]