# Generated by Django 2.2.5 on 2019-11-29 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='publisher',
            field=models.UUIDField(null=True),
        ),
    ]