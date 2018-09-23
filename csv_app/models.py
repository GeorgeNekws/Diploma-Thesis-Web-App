# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Transcr_extra_info(models.Model):
    strand = models.IntegerField()
    gene_id = models.CharField(max_length=30)
    transcr_id = models.CharField(max_length=40)
    five_utr_start = models.IntegerField(default = 0)
    five_utr_stop = models.IntegerField(default = 0)
    three_utr_start = models.IntegerField(default = 0)
    three_utr_stop = models.IntegerField(default = 0)
    genomic_coding_start = models.IntegerField(default = 0)
    genomic_coding_stop = models.IntegerField(default = 0)

    def __str__(self):
        return(self.transcr_id)

class MyChromosome(models.Model):
    chromosome_num = models.CharField(max_length=3)
    arm = models.CharField(max_length=2)
    band = models.FloatField()
    bp_start = models.IntegerField()
    bp_stop = models.IntegerField()
    stain = models.CharField(max_length=8)
    density = models.IntegerField(default = 0)

    def __str__(self):
        return(self.chromosome_num)

class Annotation(models.Model):
    chromosome = models.CharField(max_length=2)
    a_type = models.CharField(max_length=10)
    start = models.CharField(max_length=30)
    stop = models.CharField(max_length=30)
    strand = models.CharField(max_length=2)
    gene_id = models.CharField(max_length=30)
    gene_name = models.CharField(max_length=30)
    transcript_id = models.CharField(max_length=40, default='null')
    transcript_name = models.CharField(max_length=40, default='null')

    def __str__(self):
        return(self.a_type)

    # class Meta:
    #     ordering = ('')


class Mirna(models.Model):
    mirna_name = models.CharField(max_length=32, primary_key=True)
    mirna_id = models.CharField(max_length=30)
    mirna_sequence = models.CharField(max_length=30)
    mirna_family = models.CharField(max_length=300)
    mirna_seed = models.CharField(max_length=30)

    def __str__(self):
        return(self.mirna_name)


class Interaction(models.Model):

    BIND_SITE_CHOICES = (
        ('UTR3', 'UTR3'),
        ('CDS', 'CDS'),
    )

    BIND_TYPE_CHOICES = (
        ('6mer', '6mer'),
        ('7mer', '7mer'),
        ('8mer', '8mer'),
        ('9mer', '9mer'),
        ('8mer+mismatch', '8mer+mismatch'),
        ('8mer+wobble', '8mer+wobble'),
    )

    SPECIES_CHOICES = (
        ('panTro2', 'panTro2'),
        ('rheMac2', 'rheMac2'),
        ('oryCun2', 'oryCun2'),
        ('canFam2', 'canFam2'),
        ('dasNov2', 'dasNov2'),
        ('loxAfr3', 'loxAfr3'),
        ('echTel1', 'echTel1'),
        ('monDom5', 'monDom5'),
        ('mm9', 'mm9'),
        ('bosTau4', 'bosTau4'),
        ('rn4', 'rn4'),
        ('galGal3', 'galGal3'),
        ('danRer6', 'danRer6'),
        ('xenTro2', 'xenTro2'),
        ('fr2', 'fr2'),
        ('tetNig2', 'tetNig2'),
        ('NA', 'NA'),
        ('Not Conserved', 'Not Conserved'),
    )

    chromosome = models.CharField(max_length=4)
    bind_start = models.CharField(max_length=40)
    bind_stop = models.CharField(max_length=40)
    mirna_name = models.CharField(max_length=33)
    mirna_conn = models.ForeignKey('Mirna', null=True)
    gene_id = models.CharField(max_length=30)
    transcript_id = models.CharField(max_length=30)
    bind_site = models.CharField(max_length=10)
    score = models.FloatField()
    strand = models.CharField(max_length=3)
    num_species_conserved = models.CharField(max_length=4)
    species = models.CharField(max_length=250)
    bind_type = models.CharField(max_length=20)

    def __str__(self):
        return(self.mirna_name)
