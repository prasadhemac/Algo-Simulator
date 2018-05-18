import xlrd
import db_hill_climb
import all_the_combinations
import hill_climber_two_phases
import hill_climber_two_phases_with_sorting
import os

path_to_script = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(path_to_script, "output.txt")
filename1 = os.path.join(path_to_script, "output1.txt")
input = os.path.join(path_to_script, "Block Auction Algo Simulater.xlsx")

workbook = xlrd.open_workbook(input)

no_of_sheets = workbook.nsheets
f = open(filename, 'w')
f.write("\nExecuting Scenarios\n-------------------")
f.close()
f1 = open(filename1, 'w')
f1.write("\nExecuting Scenarios\n-------------------")
f1.write("\n\n\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")
f1.write("\n|\tScenario\t|\tNormal Hill Climber\t\t\t\t|\tTwo Phase Hill Climber\t\t\t|\tTwo Phase Sorted Hill Climb\t\t|\tAll The Combinations\t\t\t|")
f1.write("\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")
f1.write("\n|\t\t\t\t|\tQO Filled\t|\tExec Qty\t\t|\tQO Filled\t|\tExec Qty\t\t|\tQO Filled\t|\tExec Qty\t\t|\tQO Filled\t|\tExec Qty\t\t|")
f1.write("\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")
f1.write("\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")
f1.write("\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")
	
f1.close()
	
def printTab(len, f):

	if(len < 4):
		f.write("\t")
	if(len < 8):
		f.write("\t")
	if(len < 12):
		f.write("\t")
	
		
	return;

for i in range(0, workbook.nsheets):
	sheet = workbook.sheet_by_index(i)
	f = open(filename, 'a')
	f.write("\n\n\n"+str(i+1)+". "+ sheet.name + "\n\n")
	f.close()
	
	print("\n\n********************  Scenraio "+ str(i+1) + "  ***********************\n\n")
	
	f1 = open(filename1, 'a')
	f1.write("\n|\t"+ sheet.name + "\t\t")
	
	isQOFilled, exec_qty = db_hill_climb.processSheet(sheet, filename)
	if(isQOFilled == 1):
		f1.write("|\tYES\t\t\t")
	else:
		f1.write("|\tNO\t\t\t")
	
	f1.write("|\t" + str( exec_qty) + "\t")
	printTab(len(str(exec_qty)), f1)
	
	isQOFilled, exec_qty = hill_climber_two_phases.processSheet(sheet, filename)
	if(isQOFilled == 1):
		f1.write("|\tYES\t\t\t")
	else:
		f1.write("|\tNO\t\t\t")
	
	f1.write("|\t" + str( exec_qty) + "\t")
	printTab(len(str(exec_qty)), f1)
	
	hill_climber_two_phases_with_sorting.processSheet(sheet, filename)
	
	if(isQOFilled == 1):
		f1.write("|\tYES\t\t\t")
	else:
		f1.write("|\tNO\t\t\t")
	
	f1.write("|\t" + str( exec_qty) + "\t")
	printTab(len(str(exec_qty)), f1)
	
	isQOFilled, exec_qty = all_the_combinations.processSheet(sheet, filename)
	
	if(isQOFilled == 1):
		f1.write("|\tYES\t\t\t")
	else:
		f1.write("|\tNO\t\t\t")
	
	f1.write("|\t" + str( exec_qty) + "\t")
	printTab(len(str(exec_qty)), f1)
	
	f1.write("|")
	f1.write("\n+---------------------------------------------------------------------------------------------------------------------------------------------------------------+")

	
	f1.close
	
	f = open(filename, 'a')
	f.write("\n\n\n**************************************************************************************************************")
	f.close()
	
