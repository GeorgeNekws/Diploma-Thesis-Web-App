# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from copy import deepcopy
import models
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from csv_app.models import Interaction,Annotation,MyChromosome,Transcr_extra_info
from csv_app.forms import SpeciesSelectionForm
from django.db.models import Q
import operator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
import requests


#######################################################################################################################
def help(request):
    return render(request, 'csv_app/help.html')
#######################################################################################################################

#######################################################################################################################
def get_bind_site_choices():
    choices = ['']
    for choice in Interaction.BIND_SITE_CHOICES:
        choices.append(choice[0])
    return choices

def get_species_choices():
    choices = ['']
    for choice in Interaction.SPECIES_CHOICES:
        choices.append(choice[0])
    return choices

def get_bind_type_choices():
    choices = ['']
    for choice in Interaction.BIND_TYPE_CHOICES:
        choices.append(choice[0])
    return choices
#######################################################################################################################

@csrf_protect
def home(request):
    bind_site_list = get_bind_site_choices()
    species_list = get_species_choices()
    bind_types_list = get_bind_type_choices()

    args = {'bind_sites' : bind_site_list,
            'species' : species_list,
            'bind_types_list' : bind_types_list,
            }
    return render(request, 'csv_app/home2.html', args)


#######################################################################################################################
#default values:
    #score = 0.85
    #species = all
    #bind site = both UTR3 and CDS
    #bind type = all (6mer, 7mer, ...)
#######################################################################################################################
def data_search(request):
    q_search = request.POST.get('user_data')
    data_type = request.POST.get('user_data_type')

    mir_bool = request.POST.get('mir_bool')
    specific_mirna = request.POST.get('mirna')

    q_score = request.POST.get('the_score')
    q_site = request.POST.get('the_site')
    q_num_conserved = request.POST.get('the_num_of_conserved')
    q_species = request.POST.getlist('the_species[]')
    q_bind_types = request.POST.getlist('the_bind_types[]')

    #print 'BIND TYPES:'
    #print q_bind_types

    q_search =  q_search.replace(" ", "")   #take out any spaces from string

    if data_type == 'gene':
        q = gene_input_manipulation(q_search)
        return JsonResponse(q,safe=False)
    elif data_type == 'transcript':
        print specific_mirna
        print mir_bool
        q = transcript_input_manipulation(q_search, q_score, q_site, q_num_conserved, q_species, q_bind_types, mir_bool, specific_mirna)
        return JsonResponse(q,safe=False)
    else: # data_type == mirna
        q = mirna_input_manipulation(q_search, q_score)
        return JsonResponse(q,safe=False)


#######################################################################################################################

def mirna_input_manipulation(req_mirna, q_score):

    # default score = 0.85
    if not q_score:
        q_score = 0.85

    q1 = Interaction.objects.order_by( 'chromosome','-score').filter(
        Q(mirna_name__icontains = req_mirna, score__gte = q_score) |
        Q(mirna_conn__mirna_id__icontains = req_mirna , score__gte = q_score)               #an dwsei id anti gia onoma (icontains : contains gia substr , mporousa na xrisimopoiisw kai iexact , i : case insensitive)
    ).values('transcript_id' , 'gene_id', 'score', 'chromosome', 'mirna_name').distinct()   #edw kataxristika epistrefw to mirna name toses fores ,mono mia fora to xreiazomai gt einai idio gia oles tiw egrafes pou epistrefw

    q1 = list(q1)                                                                                #apla protimisa na min kanw allo query 3exwristo
    #print 'AVAILABLE miRNAS:'
    #print q1
    #print len(q1)

    if q1 == []:
        print 'NO MIRNAS RECORDS FOUND'
        return 'No records found'

    return q1


#######################################################################################################################

def gene_input_manipulation(gene):

    q1 = Annotation.objects.filter(
        Q(a_type = 'transcript', gene_id__icontains = gene) |   # occasion 1 , gene id is given
        Q(a_type = 'transcript', gene_name__icontains = gene)   # occasion 2 , gene name is given
    ).values('transcript_id', 'transcript_name')

    # print 'AVAILABLE TRANSCRIPTS FOR GIVEN GENE:'
    # print q1
    # print type(q1)
    q1 = list(q1)
    #print q1

    if q1 == []:
        print 'NO GENE RECORDS FOUND'
        return 'No records found'

    return q1


#######################################################################################################################

def transcript_input_manipulation(transcript, q_score, q_site, q_num_conserved, q_species, q_bind_types, mir_bool, mirna):
    #(1) for "species" checkbox choices
    # if "species" not specified , by default all species are searched ( Q()
    species = Q()
    if q_species:
        for sp in q_species:
            species |= Q(species__icontains = sp)
    #print species

    #(2) for "bind type" checkbox choices
    # bind_types = Q(bind_type__icontains = "7mer") | Q(bind_type__icontains = "8mer") | Q(bind_type__icontains = "9mer") | Q(bind_type__icontains = "8mer+mismatch") | Q(bind_type__icontains = "8mer+wobble") #DEFAULT VALUE
    # if "bind types" not specified , by default ALL are searched
    bind_types = Q();
    if q_bind_types:
        bind_types = Q()
        for bt in q_bind_types:
            bind_types |= Q(bind_type__icontains = bt)
    #print 'BIND TYPES SELECTED: '
    #print bind_types


    #(3) check if q_score is given , else give a default value
    if not q_score:
        q_score = 0.85  #default search value


    #change to check list , so i can choose both utr and cds
    #(4) if bind_site is not specified , search both UTR3 and CDS
    if not q_site:
        site = Q(bind_site__icontains = "CDS") | Q(bind_site__icontains = "UTR3") #DEFAULT VALUE
    else:
        site = Q(bind_site__icontains = q_site)
    #print site


    #(5)############## if number of conserved species not specified ,search all ############
    #in case user does not specify an input , in regex_pattern var , the q_num_conserved is 0
    #re{ n,} : Matches n or more occurrences of preceding expression.
    if not q_num_conserved:
        q_num_conserved = 0 #result even if none species is conserved
    else:
        q_num_conserved = int(q_num_conserved) - 1
        #print type(q_num_conserved)
    regex_pattern = "(\w+\,){" + str(q_num_conserved) + ",}"
    #print regex_pattern



    ##################################################  QUERIES HERE #######################################################

    # 0st. MIRNA INFO interactions
    if mir_bool == '1': #in case the user gave as an input a mirna ,and then a transcript was chosen, we have to return only the records that are related to the given mirna and transcript
        print 'MIR BOOL'
        queryset_list = Interaction.objects.filter(site, bind_types, species,   #.order_by('-score')
            Q(transcript_id__icontains = transcript , mirna_name__icontains =  mirna) , score__gte = q_score , species__regex=regex_pattern
        ).values('mirna_conn__mirna_family', 'mirna_conn__mirna_sequence', 'mirna_conn__mirna_id', 'mirna_conn__mirna_seed', 'chromosome', 'bind_start',\
        'bind_stop', 'mirna_name', 'transcript_id' , 'bind_site',\
        'score', 'strand', 'num_species_conserved', 'species', 'bind_type')
    else:   #return all the mirna interactions associated with the given gene
        queryset_list = Interaction.objects.filter(site, bind_types, species,   #.order_by('-score')
            Q(transcript_id__icontains = transcript) , score__gte = q_score , species__regex=regex_pattern
        ).values('mirna_conn__mirna_family', 'mirna_conn__mirna_sequence', 'mirna_conn__mirna_id', 'mirna_conn__mirna_seed', 'chromosome', 'bind_start',\
         'bind_stop', 'mirna_name', 'transcript_id' , 'bind_site',\
         'score', 'strand', 'num_species_conserved', 'species', 'bind_type')

    #print 'RETURNED INTERACTIONS:'
    #print queryset_list
    #print len(list(queryset_list))

    #in case no records are returned from the firs query, we query the DB again but this time with a lower default score va;ue --> 0.5
    if list(queryset_list) == []:
        print 'NO INTERACTION RECORDS FOUND'
        print 'Searching for interactions with a lower default score'

        if mir_bool == '1': #in case the user gave as an input a mirna ,and then a transcript was chosen, we have to return only the records that are related to the given mirna and transcript
            print 'MIR BOOL'
            queryset_list = Interaction.objects.filter(site, bind_types, species,   #.order_by('-score')
                Q(transcript_id__icontains = transcript , mirna_name__icontains =  mirna) , species__regex=regex_pattern
            ).values('mirna_conn__mirna_family', 'mirna_conn__mirna_sequence', 'mirna_conn__mirna_id', 'mirna_conn__mirna_seed', 'chromosome', 'bind_start',\
            'bind_stop', 'mirna_name', 'transcript_id' , 'bind_site',\
            'score', 'strand', 'num_species_conserved', 'species', 'bind_type')
        else:   #return all the mirna interactions associated with the given gene
            queryset_list = Interaction.objects.filter(site, bind_types, species,   #.order_by('-score')
                Q(transcript_id__icontains = transcript) , species__regex=regex_pattern
            ).values('mirna_conn__mirna_family', 'mirna_conn__mirna_sequence', 'mirna_conn__mirna_id', 'mirna_conn__mirna_seed', 'chromosome', 'bind_start',\
             'bind_stop', 'mirna_name', 'transcript_id' , 'bind_site',\
             'score', 'strand', 'num_species_conserved', 'species', 'bind_type')

        #if the second time we still have no records , return an appropriate message
        if list(queryset_list) == []:
            print 'INTERACTION RECORDS DO NOT EXIST (with the lowest default score = 0.5)'
            return 'No records found'


    # 1st. TRANSCRIPT INFO like start,stop,transcript name and also gene ID ,using the transcript ID
    q1 = Annotation.objects.filter(
        Q(a_type = 'transcript', transcript_id__icontains = transcript)
    ).values('start','stop','gene_id','transcript_name')
    mydict = q1[0]
    id_gene =  mydict['gene_id']


    # 2nd. GENE INFO like : gene start and stop positions , gene name based on #1 query
    q2 = Annotation.objects.filter(
        Q(gene_id = id_gene , a_type = 'gene')
    ).values('a_type', 'start', 'stop', 'chromosome', 'gene_name', 'strand')

    mydict2 = q2[0]
    #print mydict2
    chromo = mydict2['chromosome']


    # 3rd. CHROMOSOME INFO
    q3 = MyChromosome.objects.filter(
        Q(chromosome_num = chromo)
    ).values('chromosome_num', 'arm', 'band', 'bp_start', 'bp_stop', 'stain', 'density')
    #print list(q3)

    args3 = find_min_max_mirna_positions(list(queryset_list))
    # print '----------------------'
    # print args3['min_mirna_pos']
    # print args3['max_mirna_pos']
    # print '----------------------'

    min_mirna_pos = args3['min_mirna_pos']
    max_mirna_pos = args3['max_mirna_pos']


    # 4th. EXTRA INFO about trancript 3utr,5utr,.....  OCCASION 1) SHOW ALL REGIONS OF TRANSCRIPT
    q4 = Transcr_extra_info.objects.filter(
        Q(transcr_id__icontains = transcript)
    ).values('five_utr_start','five_utr_stop','three_utr_start','three_utr_stop','genomic_coding_start','genomic_coding_stop', 'strand')
    # print '************************* Q4 *********************************'
    # print list(q4)
    #check if q4 is null then return q4 = {}  , empty list !!!!!!!!! i handle it in home2-p5.js - draw_the_transcipt_regions


    # 5th. EXTRA INFO about trancript 3utr,5utr,.....   OCCASION 2) SHOW ONLY REGIONS OF TRANSCRIPT , WHERE MIRNAS ARE BOUND AND THE REGIONS BETWEEN THEM
    q9 = Transcr_extra_info.objects.filter(
        Q(transcr_id__icontains = transcript ) &
        ( Q(five_utr_stop__gte = min_mirna_pos) | Q(three_utr_stop__gte = min_mirna_pos) | Q(genomic_coding_stop__gte = min_mirna_pos) ) &
        ((Q(five_utr_start__lt = max_mirna_pos) & Q(five_utr_start__gt = 0)) |
        (Q(three_utr_start__lt = max_mirna_pos) & Q(three_utr_start__gt = 0)) | (Q(genomic_coding_start__lt = max_mirna_pos) & Q(genomic_coding_start__gt = 0)))
    ).values('five_utr_start','five_utr_stop','three_utr_start','three_utr_stop','genomic_coding_start','genomic_coding_stop', 'strand')
    # print '************************* Q9 *********************************'
    # print list(q9)


    args = {
        'transcript_start' : mydict['start'],
        'transcript_stop' : mydict['stop'],
        'a_type' : mydict2.get('a_type'),
        'gene_start' : mydict2.get('start'),
        'gene_stop' : mydict2.get('stop'),
        'gene_chromosome' : mydict2.get('chromosome'),
        'gene_identifier' : id_gene,
        'gene_name' : mydict2.get('gene_name'),
        'gene_strand' : mydict2.get('strand'),
    }

    q = list(queryset_list)

    # find the 'min' and the 'new length' for regions(utr,cds) that are bound by mirnas (ONLY)
    args2 = make_calculations(list(queryset_list), list(q9))    #changed from q4 to q9
    args.update(args2)

    #find the 'min' and the 'new_length', to draw the transcript with all the utr,cds regions and not only the binding ones
    args4 = make_calculations(list(queryset_list), list(q4))
    args4['el2'] = args4.pop('min')
    args4['nl2'] = args4.pop('new_length')
    args.update(args4)

    #In order not to pass the list-argument BY reference , but as values
    fun_param = q[:]
    fun_param2 = deepcopy(q)

    families = check_for_families(fun_param2)
    families2 = check_for_duplicates(families) #if i pass as an argument the list 'families' , then families will be the same as families2 . If i want not to be the same i have to make a deepcopy like above

    q.insert(0,args)
    q.insert(1,list(q3)) #chromosome info append to returned data list
    q.insert(2,list(q9)) #5'utr, 3'utr, cds, ... info append to returned data list
    q.insert(3,families)
    q.insert(4,list(q4)) #all regions 5utr, 3utr, cds , not only the bound by mirnas like q9


    # print' ---------------- Q ---------------------------'
    # print q
    # print len(q)

    # print' ---------------- FAMILIES ---------------------------'
    #print families
    # print len(families)

    stats = compute_statistics(q)
    #print stats
    q.insert(5,stats)

     #                               args    chromosome     5utr,3utr       families      all_regions     stats       mirnas(queryset_list)
     #list : q has a format like q= [{} , [{},{},{},{}] ,   [{},{},{}] ,   [{},{}..],      [{}.{}...],     {}              {},{},{}.....        ]
    return q


#######################################################################################################################

def compute_statistics(json):
    unique_mirnas_name_list = []
    unique_family_names = []
    res_conserved_species_list = []
    res_bind_site_list = []
    utr_3_list = []
    cds_list = []
    res_bind_types_list = []
    unique_species_list = []
    unique_bind_types_list = []

    res_max_bind_len = 0
    res_min_bind_len = 1000000000
    all_distances = 0

    dict_species = {}
    dict_bind_type = {}
    dict_family = {}    #MREs per family eg. let-7f-2-3p/1185-3p : [hsa-let-7f-2-3p', hsa-let-7f-2-3p', hsa-miR-1185-1-3p', hsa-miR-1185-2-3p', hsa-miR-1185-1-3p', hsa-miR-1185-2-3p', hsa-miR-1185-1-3p', hsa-miR-1185-2-3p']


    #-----------------------------------------------------------------------------------------------------#
    familia = json[3]
    for i in range(0,len(familia)):
        if familia[i]['mirna_conn__mirna_family'] not in unique_family_names:
            dict_family[familia[i]['mirna_conn__mirna_family']] = []
            unique_family_names.append(familia[i]['mirna_conn__mirna_family'])
        #dict_family[familia[i]['mirna_conn__mirna_family']] = 0
        for j in range(0,len(familia[i]['mirna_name'])):
            dict_family[familia[i]['mirna_conn__mirna_family']].append(familia[i]['mirna_name'][j])

    # print '\n'
    # print 'Families interact with this miTG : ' , unique_family_names
    # print '\n'
    # for  index in dict_family:
    #     print index , " : " , dict_family[index] , "\n"
    #-----------------------------------------------------------------------------------------------------#


    for i in range(5,len(json)):
        #-----------------------------------------------------------------------------------------------------#

        #1. find how many unique microRNAs bind to the given transcript ,store the names to a list-array
        if json[i]['mirna_name'] not in unique_mirnas_name_list:
            unique_mirnas_name_list.append(json[i]['mirna_name'])

        #-----------------------------------------------------------------------------------------------------#

        #2. find which species exist in this Interaction in res_conserved_species_list , exist all the records of species with duplicates
        # i show to the user all the different species that participate to his search and their frequency.
        myArray = json[i]['species'].split(',')        #example : json[i]['species'] =  panTro2,rheMac2,monDom5
        for j in range(0,len(myArray)):
            res_conserved_species_list.append(myArray[j])

            if myArray[j] not in unique_species_list:  #unique records of species
                unique_species_list.append(myArray[j])
        #print "Species that interact : " , unique_species_list

        #-----------------------------------------------------------------------------------------------------#

        #3. list containing all bind sites - so then i can find how many results are bound in UTR3 and how many in CDS
        res_bind_site_list.append(json[i]['bind_site'])
        # separetely in 3utr , cds lists
        if json[i]['bind_site'] == 'UTR3':
            utr_3_list.append(json[i]['bind_site'])
        else:
            cds_list.append(json[i]['bind_site'])

        #print 'number of 3utr interactions : ' , len(utr_3_list)
        #print 'number of cds interactions : ' , len(cds_list)

        #-----------------------------------------------------------------------------------------------------#

        #4.find all the bind types of this interaction
        res_bind_types_list.append(json[i]['bind_type'])

        if json[i]['bind_type'] not in unique_bind_types_list:     #unique records of bind types
            unique_bind_types_list.append(json[i]['bind_type'])
        #print "Bind types that occur in interactions : " , unique_bind_types_list

        #-----------------------------------------------------------------------------------------------------#

        #5. find the min,max,avg bind length to the given transcript
        if ';' in json[i]['bind_start']:       #LABEL : semicolon
            #calculate distance of binding --> there are 2 parts of binding and between the intron
            dist = (int(json[i]['bind_stop'].split(';')[0]) - int(json[i]['bind_start'].split(';')[0]) +1 ) + ( int(json[i]['bind_stop'].split(';')[1]) - int(json[i]['bind_start'].split(';')[1]) +1)
        else:
            dist = int(json[i]['bind_stop']) - int(json[i]['bind_start']) + 1

        if dist < res_min_bind_len:
          res_min_bind_len = dist

        if dist > res_max_bind_len:
          res_max_bind_len = dist

        all_distances = all_distances + dist

        #print 'min bind len distance : ' , res_min_bind_len
        #print 'max bind len distance : ' , res_max_bind_len

        #-----------------------------------------------------------------------------------------------------#


    #1. -------------------------------- microRNAs NAMES   ----------------------------------------------------#
    #print len(unique_mirnas_name_list) , " number of unique microRNAs that interact"

    #-----------------------------------------------------------------------------------------------------#

    #2. find the frequency of the species for this transcript
    #final result will be smth like: dict = {panTro2 : 10 , loxAfr3 : 23 , .....}
    for j in range(0,len(unique_species_list)):
        dict_species[unique_species_list[j]] = 0
        for k in range(0,len(res_conserved_species_list)):
            if res_conserved_species_list[k] == unique_species_list[j]:
                dict_species[unique_species_list[j]] = dict_species[unique_species_list[j]] + 1

    # print "Number of different species that are conserved for the given transcript " , len(unique_species_list)
    # for  index in dict_species:
    #     print index , " : " , dict_species[index] , "\n"

    #-----------------------------------------------------------------------------------------------------#

    #--------------------------------   BIND SITE --------------------------------------------------------#
    #3. find the frequency of UTR3 and CDS
    utr3_prob = float( len(utr_3_list)) / float((len(json)-5))
    utr3_prob = "{:.2f}".format(utr3_prob)
    cds_prob = float( len(cds_list)) / float((len(json)-5))
    cds_prob = "{:.2f}".format(cds_prob)
    # print "Probability to bind to UTR3 is :" , utr3_prob , "\n"
    # print "Probability to bind to CDS is :" , cds_prob , "\n"

    #-----------------------------------------------------------------------------------------------------#

    #--------------------------------   BIND TYPE --------------------------------------------------------#
    #4. find the frequency of Bind Types
    # res_bind_types_list = [6mer, 6mer, 7mer, 8mer, 7mer]
    # unique_bind_types_list = [6mer,7mer,8mer]
    for j in range(0,len(unique_bind_types_list)):
        dict_bind_type[unique_bind_types_list[j]] = 0
        for k in range(0,len(res_bind_types_list)):
            if res_bind_types_list[k] == unique_bind_types_list[j]:
                dict_bind_type[unique_bind_types_list[j]] = dict_bind_type[unique_bind_types_list[j]] + 1
    # for index in dict_bind_type:
    #     print index , " : " , dict_bind_type[index] , "\n"

    #-----------------------------------------------------------------------------------------------------#

    #5. MIN , MAX , AVG bind lengths
    # print 'min bind length : ' , res_min_bind_len
    # print 'max bind length : ' , res_max_bind_len
    res_avg_bind_len = all_distances / (len(json) - 5)
    #print 'avg bind length : ' , res_avg_bind_len

    #-----------------------------------------------------------------------------------------------------#

    stats = {
        #'unique_family_names' : unique_family_names ,              take the values from dict_family (keys)
        #'unique_bind_types_list' : unique_bind_types_list ,        take the values from dict_bind_type (keys)
        #'unique_species_list' : unique_species_list ,              take the values from dict_species (keys)
        'unique_mirnas_name_list' : unique_mirnas_name_list ,

        'families_contain': dict_family ,
        'bind_type_dict' : dict_bind_type ,
        'species_dict' : dict_species ,

        'utr3_prob' : utr3_prob ,
        'cds_prob' : cds_prob ,
        'min_bind_len' : res_min_bind_len ,
        'max_bind_len' : res_max_bind_len ,
        'avg_bind_len' : res_avg_bind_len ,
    }

    return stats


#######################################################################################################################

#function: for instance if there is ['UTR3' , 'UTR3'] in a query record , then i change it to ['UTR3']
def check_for_duplicates(families):
    #print type(families)
    for i in range(0,len(families)):
        # print i
        # print families[i]['bind_type']
        # print families[i]['bind_site']
        # print families[i]['mirna_conn__mirna_seed']
        families[i]['bind_type'] = list(set( families[i]['bind_type']))
        families[i]['bind_site'] = list(set( families[i]['bind_site']))
        families[i]['num_species_conserved'] = list(set( families[i]['num_species_conserved']))
        families[i]['mirna_conn__mirna_seed'] = list(set( families[i]['mirna_conn__mirna_seed']))
        families[i]['score'] = max(families[i]['score'])    #i return always the highest score in families
        # print families[i]['bind_type']
        # print families[i]['bind_site']
        # print families[i]['mirna_conn__mirna_seed']


#######################################################################################################################

#if 2 or more mirnas belong to the same family and start at the same position , then merge them in one record
def check_for_families(mirnas):
    index_to_delete = []    #after grouping by some records because of the same family and bind start , we delete some records (the merged)

    for i in range(0,len(mirnas)):
        if i+1 > len(mirnas):
            break

        mirnas[i]['mirna_name'] = [ mirnas[i]['mirna_name'] ]
        mirnas[i]['mirna_conn__mirna_sequence'] = [ mirnas[i]['mirna_conn__mirna_sequence'] ]
        mirnas[i]['mirna_conn__mirna_seed'] = [ mirnas[i]['mirna_conn__mirna_seed'] ]
        mirnas[i]['mirna_conn__mirna_id'] = [ mirnas[i]['mirna_conn__mirna_id'] ]
        mirnas[i]['score'] = [ mirnas[i]['score'] ]
        mirnas[i]['bind_type'] = [ mirnas[i]['bind_type'] ]
        mirnas[i]['bind_site'] = [ mirnas[i]['bind_site'] ]
        mirnas[i]['species'] = [ mirnas[i]['species'] ]
        mirnas[i]['num_species_conserved'] = [ mirnas[i]['num_species_conserved'] ]
        mirnas[i]['bind_stop'] = [ mirnas[i]['bind_stop'] ]
        mirnas[i]['merged_in_family'] = 0
        mirnas[i]['same_family'] = 0

        for j in range(i+1,len(mirnas)):
            #print 'i : '+ str(i)
            #print 'j : '+ str(j)

            #LABEL : semicolon
            # i just put the mirnas[i or j]['bind_start'] in variables in order to check if the coordinates contain a semicolon ';', if they do i take into account the very first start
            mirna_j_start = mirnas[j]['bind_start']
            mirna_i_start = mirnas[i]['bind_start']
            if ';' in mirnas[i]['bind_start']:
                mirna_i_start = mirnas[i]['bind_start'].split(';')[0]
            if ';' in mirnas[j]['bind_start']:
                mirna_j_start = mirnas[j]['bind_start'].split(';')[0]

            if mirnas[i]['mirna_conn__mirna_family'] == mirnas[j]['mirna_conn__mirna_family']:      # if the mirnas belong to the same family
                mirnas[i]['same_family'] = 1                                                        # this variable is 1 when at least 2 records have same family , but it is NOT obligatory to be merged
                #if mirnas[i]['bind_start'] == mirnas[j]['bind_start']:                              # AND if the mirnas have the same bind_start , THEN: MERGE these 2 records i,j
                if mirna_i_start  == mirna_j_start:               #LABEL : semicolon               # AND if the mirnas have the same bind_start , THEN: MERGE these 2 records i,j
                    mirnas[i]['merged_in_family'] = 1   # AND turn this variable to 1 (this variable is 1 when at least 2 records are merged (that means they have same start pos and belong to the same family))

                    if j not in index_to_delete:
                        index_to_delete.append(j)

                    mirnas[i]['mirna_name'].append(mirnas[j]['mirna_name'])
                    mirnas[i]['mirna_conn__mirna_sequence'].append(mirnas[j]['mirna_conn__mirna_sequence'])
                    mirnas[i]['mirna_conn__mirna_seed'].append(mirnas[j]['mirna_conn__mirna_seed'])
                    mirnas[i]['mirna_conn__mirna_id'].append(mirnas[j]['mirna_conn__mirna_id'])
                    mirnas[i]['score'].append(mirnas[j]['score'])
                    mirnas[i]['bind_type'].append(mirnas[j]['bind_type'])
                    mirnas[i]['bind_site'].append(mirnas[j]['bind_site'])
                    mirnas[i]['species'].append(mirnas[j]['species'])
                    mirnas[i]['num_species_conserved'].append(mirnas[j]['num_species_conserved'])
                    #mirnas[i]['bind_stop'].append(mirnas[j]['bind_stop'])

                    if ';' in mirnas[j]['bind_stop']:   #if in bind_stop exist a ';' i take into account the very last end
                        mirnas[i]['bind_stop'].append(mirnas[j]['bind_stop'].split(';')[1])
                    else:
                        mirnas[i]['bind_stop'].append(mirnas[j]['bind_stop'])

                    #print '*******************************'
                    #print mirnas[i]['mirna_name']

                    #     'transcript_id' : [mirnas[i]['transcript_id']],
                    #     'strand' : mirnas[i]['strand'],
                    #     'chromosome' : mirnas[i]['chromosome'],
                    #     'mirna_conn__mirna_family' : mirnas[i]['mirna_conn__mirna_family'],
                    #     'bind_start' : mirnas[i]['bind_start'],


        index_to_delete.sort(reverse=True)      #delete some records after the merging
        for i in range(0,len(index_to_delete)):
            mirnas.pop(index_to_delete[i])
        index_to_delete = []

    #print mirnas
    #print len(mirnas)
    return mirnas


#######################################################################################################################

#find the min and the max position on the chr that a mirna is bound (among all the mirnas)
def find_min_max_mirna_positions(mirna):
    max=0
    min = 900000000 #smallest numeric position that a mirna starts on chr

    #print (json[3]['bind_stop'])
    for i in range(0,len(mirna)):

        #LABEL : semicolon
        if ';' in mirna[i]['bind_stop']:
            if int(mirna[i]['bind_stop'].split(';')[1]) > max:
                max = int(mirna[i]['bind_stop'].split(';')[1])

            if int(mirna[i]['bind_start'].split(';')[0]) < min:
                min = int(mirna[i]['bind_start'].split(';')[0])
        else:
            if int(mirna[i]['bind_stop']) > max:
                max = int(mirna[i]['bind_stop'])

            if int(mirna[i]['bind_start']) < min:
                min = int(mirna[i]['bind_start'])

    new_length = max - min + 1
    # print  min
    # print  max

    args = {'min_mirna_pos' : min,
            'max_mirna_pos' : max,
    }
    return args


#######################################################################################################################

def make_calculations(mirna,tr_region):

    max=0
    min = 900000000
    #In general when i have a STRAIGHT strand , the trans_region is sequentially 5utr , cds , 3utr
    #q9 may return results that include only 3utr coordinates or 3utr and cds coordinates for example
    #so, i have to take into account these cases when i search for the min
    #similarly for the max and when i have an opposite strand



    for i in range(0,len(tr_region)):

        if ((tr_region[i]['five_utr_start'] < min) and (tr_region[i]['five_utr_start'] !=0)):
            min = tr_region[i]['five_utr_start']
        if ((tr_region[i]['three_utr_start'] < min) and (tr_region[i]['three_utr_start'] !=0)):
            min = tr_region[i]['three_utr_start']
        if ((tr_region[i]['genomic_coding_start'] < min) and (tr_region[i]['genomic_coding_start'] !=0)):
            min = tr_region[i]['genomic_coding_start']

        if (tr_region[i]['three_utr_stop'] > max ):
            max = tr_region[i]['three_utr_stop']
            #print 'INSIDE MAX !!!'
        if (tr_region[i]['five_utr_stop'] > max ):
            max = tr_region[i]['five_utr_stop']
            #print 'INSIDE MAX !!!'
        if (tr_region[i]['genomic_coding_stop'] > max ):
            max = tr_region[i]['genomic_coding_stop']
            #print 'INSIDE MAX !!!'

    new_length = max - min + 1

    # print 'elaxisto2 ', min
    # print 'megisto2 ' , max
    # print 'new_length2 ', new_length2

    args = {
            'min' : min,
            'new_length' : new_length,
    }
    return args
