# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-23 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0026_transcr_extra_info'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyInteraction',
        ),
        migrations.AlterField(
            model_name='interaction',
            name='chromosome',
            field=models.IntegerField(),
        ),
    ]
