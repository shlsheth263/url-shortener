# Generated by Django 3.0.7 on 2020-06-06 07:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200606_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='short_urls',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
