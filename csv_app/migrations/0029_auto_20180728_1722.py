# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-28 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0028_auto_20180723_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='exon_id',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='exon_number',
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='relative_bind_start',
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='relative_bind_stop',
        ),
        migrations.RemoveField(
            model_name='mychromosome',
            name='iscn_start',
        ),
        migrations.RemoveField(
            model_name='mychromosome',
            name='iscn_stop',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='chromosome_name',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='exon_chr_start',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='exon_chr_stop',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='gene_name',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='gene_start',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='gene_stop',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='transcr_start',
        ),
        migrations.RemoveField(
            model_name='transcr_extra_info',
            name='transcr_stop',
        ),
        migrations.AddField(
            model_name='mirna',
            name='mirna_family',
            field=models.CharField(default='null', max_length=300),
        ),
        migrations.AddField(
            model_name='mirna',
            name='mirna_seed',
            field=models.CharField(default='null', max_length=30),
        ),
    ]
