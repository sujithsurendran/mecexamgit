import os
import csv
from fpdf import FPDF
from collections import Counter
from collections import defaultdict

def input_papers(source_file):
	paper="XXX"
	grep_str = "Student"
	dt = input("Date(dd-mm-FN/AN)?")
	while paper != "":
		paper = input("Enter paper...")
		grep_str = grep_str + "|" + paper
		if grep_str != 'Student|':
			os.system("egrep '(" + grep_str[:-1] + ")' " + source_file + " > " + dt + ".csv")
		else:
			os.system('cp ' + source_file + ' ' + dt + ".csv")
	return len(open(dt + ".csv").readlines(  )), dt
	

def fetch_rooms(students=0):

	if students == "" or students == "0":
		return nil
	
	alter = input("Alteration?")
	if alter == "":
		alter = 0
	else:
		alter = int(alter)
		
	


	details=[]
	rooms=[]
	capacities=[]
	max_capacities=[]
	current_capacities=[]

	total = 0
	
	with open("./rooms.txt") as file1:
		
		for line in file1:
			line_i = line.rstrip()
			details = line_i.split(",")
			rooms.append(details[0])
			max_capacities.append(details[2])
			current_capacities.append(details[3])

			capacity = int(details[3]) + alter
			if capacity >= students:
				capacities.append(students)
				return capacities,rooms
				#for room1, capacity1 in zip(rooms,capacities):
				#	print(room1 + "=>" + str(capacity1))
				exit()
			else:

				students = students - capacity
				if students>0:
					capacities.append(capacity)


	

students, source_file = input_papers("210831-FN.csv")
print("Student Count = " + str(students))


capacities,rooms = fetch_rooms(students)
#for room1, capacity1 in zip(rooms,capacities):
#	print(room1 + "=>" + str(capacity1))


summary=[]
counter={}
with open("./output.csv","w") as file1, open(source_file + '.csv') as file2:
	pdf = FPDF('P', 'mm', 'A4')
	
	csvReader = csv.DictReader(file2)

	writer = csv.DictWriter(file1, fieldnames = ["No","Room","Seat","Student","RegNo","Slot","Paper"])
	writer.writeheader()
	room_index=0
	for room,capacity in zip(rooms,capacities):
		
		#writer.writerow({
		#'Room':"Room: " + room,
		#'Seat':"",
		#'Student':"",
		#'RegNo':"",
		#'Slot':"",
		#'Paper':"",
		#})					
		i=1
		room_index=room_index+1
		pdf.add_page()
		pdf.set_font('Times', '', 20)
		pdf.cell(0, 10, 'Seating Arrangement - ' + source_file, 0,1,'R')
		pdf.set_font('Times', 'B', 22)
		pdf.cell(0, 10, 'Room :' + room, 0,1,'R')
		pdf.set_font('Times', 'B', 16)
		
		pdf.cell(12, 10, "Seat" , 1,0)
		pdf.cell(70, 10, "Student" , 1,0)
		pdf.cell(50, 10, "RegNo" , 1,0)
		pdf.cell(12, 10, "Slot" , 1,0)
		pdf.cell(30, 10, "Paper" , 1,1)
		
		pdf.set_font('Times', '', 16)
		
		for i,row in zip(range(1,capacity+1),csvReader):
			
	
			for rx in ('401','515','511'):
				if room == rx and row["RegNo"].strip() == 'MDL18CS066':
					
					input("LijoZechariahJames cannot sit in " + rx)
					exit()		
				

			studentName = row["Student"]
			
			if row["RegNo"].strip() in ('MDL18CS066', 'MUT18ME028'):
				studentName = " * " + studentName	


			writer.writerow({
			'No':room_index,
			'Room':room,
			'Seat':"A" + str(i).zfill(2),
			'Student':studentName,
			'RegNo':row["RegNo"],
			'Slot':row["Slot"],
			'Paper':row["Paper"],
			})	
			
			
			
			if row["RegNo"].strip() == 'MUT18ME028':
				if i != 1 and room != rooms[1]:
					input("Gokul Mohan has to be put in First Room")
					exit()
				
				


			#str_row = str(i).zfill(2) + row["Student"][0:20] +  row["RegNo"][0:15] + row["Slot"][0:2] + row["Paper"]
			#pdf.cell(0, 10, str_row, 1,1)
			
			studentName = studentName[0:25].title().replace(" ", "")
			
			pdf.cell(12, 10, "A" + str(i).zfill(2) , 1,0)
			pdf.cell(70, 10, studentName , 1,0)
			pdf.cell(50, 10, row["RegNo"] , 1,0)
			pdf.cell(12, 10, row["Slot"] , 1,0)
			pdf.cell(30, 10, row["Paper"].lstrip() , 1,1)
			i=i+1
			#summary[str(room) + row["Paper"].lstrip()] = str(room) + row["Paper"].lstrip()
			summary.append(str(room) + "^" + row["Paper"].lstrip())
			#counter[str(room) + "-" + row["Paper"].lstrip()] = str(room) + "-" + row["Paper"].lstrip()
			
	pdf.output(source_file + '.pdf', 'F')
	print("output in " + source_file + '.pdf')
	

