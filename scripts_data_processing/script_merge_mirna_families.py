
import csv

f1 = open("/home/geo/Desktop/21_final_processed_mature.fa.txt")
data = csv.reader(f1 , delimiter="	")
f2 = open("/home/geo/Desktop/processed_miR_Family_Info.txt.csv")
data2 = csv.reader(f2 , delimiter="	")

file_object = open('merged_mirna_families.txt.csv', 'w' )

#if they have the same mimat and sequence , then merge

k = 0
for row in data:
	for row2 in data2:
		if row[1] == row2[6]:
			if row[2] == row2[4]:
				bike = 1
				k = k+1
				element = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + row2[0] + '\t'+  row2[1] + '\n'
				file_object.write(element)
				break
	f2.seek(0)
print k
