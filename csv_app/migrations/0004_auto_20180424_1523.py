# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-24 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0003_auto_20180412_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='exon_id',
            field=models.CharField(default='null', max_length=30),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='exon_number',
            field=models.CharField(default='null', max_length=5),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='transcript_id',
            field=models.CharField(default='null', max_length=40),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='transcript_name',
            field=models.CharField(default='null', max_length=40),
        ),
    ]