# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0002_auto_20160802_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fowler',
            name='follow_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
