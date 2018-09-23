# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-24 10:25
from __future__ import unicode_literals

from django.db import migrations

def link_mirnas(apps, schema_editor):
    Mirna = apps.get_model('csv_app', 'Mirna')
    Interaction = apps.get_model('csv_app', 'Interaction')
    for inter in Interaction.objects.all():
        mirna, created = Mirna.objects.get_or_create(mirna_name=inter.mirna_name)
        inter.mirna_connection = mirna
        inter.save()


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0022_auto_20180624_1024'),
    ]

    operations = [
        migrations.RunPython(link_mirnas),
    ]
