
import csv 

data = csv.reader(open("/home/geo/Downloads/humanito_interactions.txt.csv"),delimiter="	")
file_object = open('human_interactions.txt', 'w' )

for row in data:
	if(float(row[4]) >= 0.5):					#if microT SCORE greater than 0.5 ,then write(keep) this record to my file
		my_list = row[3].split("|")
		my_list2 = row[6].split("|")
		
		row[0] = row[0].replace('chr','')
		
		
		
		element = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + my_list[0] + '\t' + my_list[1] + '\t' + my_list[2] + '\t' + my_list[3] + '\t' + row[4] + '\t' + row[5] + '\t' '''+ my_list2[0] + '\t' + my_list2[1] + '\t' ''' + my_list2[3] + '\t' + my_list2[4]  + '\t' + my_list2[5] +'\n'
		file_object.write(element)


file_object.close()



