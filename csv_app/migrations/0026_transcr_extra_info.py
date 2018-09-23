# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-26 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0025_transfer_mirna5'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcr_extra_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strand', models.IntegerField()),
                ('chromosome_name', models.CharField(max_length=30)),
                ('gene_name', models.CharField(max_length=30)),
                ('gene_id', models.CharField(max_length=30)),
                ('transcr_id', models.CharField(max_length=40)),
                ('gene_start', models.IntegerField()),
                ('gene_stop', models.IntegerField()),
                ('transcr_start', models.IntegerField()),
                ('transcr_stop', models.IntegerField()),
                ('five_utr_start', models.IntegerField(default=0)),
                ('five_utr_stop', models.IntegerField(default=0)),
                ('three_utr_start', models.IntegerField(default=0)),
                ('three_utr_stop', models.IntegerField(default=0)),
                ('genomic_coding_start', models.IntegerField(default=0)),
                ('genomic_coding_stop', models.IntegerField(default=0)),
                ('exon_chr_start', models.IntegerField()),
                ('exon_chr_stop', models.IntegerField()),
            ],
        ),
    ]