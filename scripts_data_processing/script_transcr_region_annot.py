
import csv 

data = csv.reader(open("/home/geo/Downloads/last2_mart_export.txt.csv"),delimiter="	")
file_object = open('biomart_transcr_region_annot.csv', 'w' )

lista = []
for i in range(1,23):
	lista.append(str(i))
lista.append('X')
lista.append('Y')
print lista

#we do not want the records that have as chr a patch
for row in data:
	if(row[17] == 'protein_coding' and (row[2] in lista) ):		
		if( row[9] =='' and row[10] =='' and row[11] =='' and row[12] =='' and row[15] =='' and row[16] =='' ):
			continue
		else:	
			element = row[0] + '\t' + row[1] + '\t' + row[7] + '\t' + row[9] + '\t' + row[10] + '\t' + row[11] + '\t' + row[12] + '\t' +\
			row[15] + '\t' + row[16] + '\n'
			file_object.write(element)


file_object.close()
