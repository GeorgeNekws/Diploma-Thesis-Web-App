# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-07 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0014_auto_20180607_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mychromosome',
            name='band',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='mychromosome',
            name='bp_start',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='mychromosome',
            name='bp_stop',
            field=models.IntegerField(),
        ),
    ]
