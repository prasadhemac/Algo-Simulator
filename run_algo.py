import xlrd
import db_hill_climb
import db_hill_climb_random
import all_the_combinations
import hill_climber_two_phases
import hill_climber_two_phases_with_sorting
import os

instrument = "BA06_B"
mid_price = 11.0
path_to_script = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(path_to_script, "output.txt")
filename1 = os.path.join(path_to_script, "bdd.txt")
input = os.path.join(path_to_script, "Block Auction Algo Simulater.xlsx")

workbook = xlrd.open_workbook(input)

no_of_sheets = workbook.nsheets
f = open(filename, 'w')
f.write("\nExecuting Scenarios\n-------------------")
f.close()

f1 = open(filename1, 'w')
f1.write("\n\n")
f1.close()
	

for i in range(0, no_of_sheets):
	sheet = workbook.sheet_by_index(i)
	#f = open(filename, 'a')
	#f.write("\n\n\n"+str(i+1)+". "+ sheet.name + "\n\n")
	#f.close()
	
	print("\n\n********************  Scenraio "+ str(i+1) + "  ***********************\n\n")
	
	
	
	db_hill_climb.processSheet(sheet, filename, filename1, instrument, mid_price)
	#all_the_combinations.processSheet(sheet, filename)
	#hill_climber_two_phases.processSheet(sheet, filename)
	#hill_climber_two_phases_with_sorting.processSheet(sheet, filename)
	
	
	f = open(filename, 'a')
	f.write("\n\n\n**************************************************************************************************************")
	f.close()
	