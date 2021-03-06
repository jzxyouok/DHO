# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0004_fowler_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fowler',
            name='OpenID',
            field=models.CharField(max_length=100, unique=True, verbose_name='\u7528\u6237ID'),
        ),
        migrations.AlterField(
            model_name='fowler',
            name='follow_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u5173\u6ce8\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='fowler',
            name='location',
            field=models.CharField(default='None', max_length=100, verbose_name='\u5730\u7406\u4f4d\u7f6e'),
        ),
    ]
