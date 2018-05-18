import xlrd
import operator
import numpy

def printLine(line):
	print(line)
	
	f = open(filename, 'a')
	  # python will convert \n to os.linesep
	#f.write('hiiiii')
	if ('numpy' in str(type(line))):
		for i in range(0, len(line[:,3])):
			for j in range(0, len(line[0, :])):
				f.write(str(line[i,j]) + "\t\t")
			f.write("\n")
	else:
		f.write(line)
	f.close() 
	
	return;
	
def printFile(line):
	
	f = open(filename, 'a')
	  # python will convert \n to os.linesep
	#f.write('hiiiii')
	if ('numpy' in str(type(line))):
		for i in range(0, len(line[:,3])):
			for j in range(0, len(line[0, :])):
				f.write(str(line[i,j]) + "\t\t")
			f.write("\n")
	else:
		f.write(line)
	f.close() 
	
	return;

def executeRemainder(agg,n, res):
	for i in range(n, len(agg[:,3])):
		printLine(agg[i,0])
		res_rem = res[:,3].astype('float').sum() - res[:,4].astype('float').sum()
		if(agg[i,2] - agg[i,4]> res_rem):
			printLine(res_rem)
			printLine("aaa")
			continue
		for j in range(0, len(res[:,3])):
			if(agg[i,3] - agg[i,4] > 0):
				if(res[j,3] - res[j,4] >0):
					exec_qty = min(agg[i,3] - agg[i,4], res[j,3] - res[j,4])
					agg[i,4] += exec_qty
					res[j,4] += exec_qty
					printLine(str(agg[i,0]) + " - " + str(res[j,0])+ ": " + str(exec_qty))
	return;
	
def checkIfLessThanMaqFilled(arr):
	for i in range(0, len(arr[:,3])):
		if(arr[i,2]> arr[i,5] and arr[i,5] > 0.0):
			return 1;
	return 0;

def applyTwoPhasesHilClimbAlgo(agg, contra):
	sideIterator = 1
	aheadQty = 0
	contra_total = 0.0
	
	for i in range(0, len(contra[:,3])):
		contra_total += contra[i,3]
			
	#print(contra_total)
	
	process = 1
	while(process == 1):
		#printLine(agg)
		#printLine(contra)
		#printLine("\n")
		
		temp = numpy.copy(agg)
		if(sideIterator > 1):
			contra_total = aheadQty

	#	printLine("\n contra total = " +str( contra_total) +"\n")
		
		if(contra_total == 0.0):
			break
			
		aheadQty = 0.0
		executableQtyOfAMesChanged = 0
		
		length = len(agg[:,3])
		for i in range(0,length):
			
			#printLine(agg[i,0])
			if(sideIterator < 3):
				agg[i, 4] = agg[i,3]
			
			avail_qty = contra_total - aheadQty
			actual_maq = min( agg[i,2], agg[i,3])
			
			if(agg[i,1] < 0):
				continue
			
			if(avail_qty > 0.0 and avail_qty >= actual_maq ):
				new_exec_size = min(avail_qty, agg[i,2])
#				if(agg[i,2] > 0.0 and new_exec_size != agg[i,4]):
#					executableQtyOfAMesChanged = 1
#					printLine("aaa")
					
				agg[i,4] = new_exec_size
				aheadQty += new_exec_size
			
			else:
				agg[i,4] = 0.0
				if(agg[i,2] > 0.0):
					executableQtyOfAMesChanged = 1
#					printLine("bbb")
				#agg = numpy.delete(agg, (i), axis = 0)
				if(agg[i,1] == 1):
					agg[i,1] = -1
				else:
					agg[i,1] = -2
		
	#	printLine("\n")
	#	printLine(agg)
	#	printLine(contra)
	#	printLine("\n")
		
		
		for i in range(0,length):
			if(agg[i,1] < 0):
				continue
			
			avail_qty = contra_total - aheadQty
			
			if(avail_qty > 0.0 ):
				new_exec_size = min(avail_qty, agg[i,3] - agg[i,4])
#				if(agg[i,2] > 0.0 and new_exec_size != agg[i,4]):
#					executableQtyOfAMesChanged = 1
#					printLine("aaa")
					
				agg[i,4] += new_exec_size
				aheadQty += new_exec_size
			
	#	printLine("\n")
	#	printLine(agg)
	#	printLine(temp)
	#	printLine("\n")
		
		for i in range(0, len(agg[:,3])):
			if( agg[i,4] != temp[i,4]):
				executableQtyOfAMesChanged = 1
						
		if(executableQtyOfAMesChanged == 0 and sideIterator >= 2):
			process = 0
		
		else:
			tmp = agg
			agg = contra
			contra = tmp
			sideIterator += 1
	
	return;
	

def applyApplyHilClimbAlgo(agg, contra):
	sideIterator = 1
	aheadQty = 0
	contra_total = contra[:,3].astype('float').sum()

	process = 1
	while(process == 1):
		# printLine(agg)
		# printLine(contra)
		if(sideIterator > 1):
			contra_total = aheadQty
			
		if(contra_total == 0.0):
			break
			
		aheadQty = 0.0
		executableQtyOfAMesChanged = 0
		
		length = len(agg[:,3])
		for i in range(0,length):
			
#			printLine(agg[i,0])
			if(sideIterator < 3):
				agg[i, 4] = agg[i,3]
			
			avail_qty = contra_total - aheadQty
			actual_maq = min( agg[i,2], agg[i,3])
			
			if(agg[i,1] < 0):
				continue
			
			if(avail_qty > 0.0 and avail_qty >= actual_maq):
				new_exec_size = min(avail_qty, agg[i,3])
				if(agg[i,2] > 0.0 and new_exec_size != agg[i,4]):
					executableQtyOfAMesChanged = 1
#					printLine("aaa")
					
				agg[i,4] = new_exec_size
				aheadQty += new_exec_size
			
			else:
				agg[i,4] = 0.0
				if(agg[i,2] > 0.0):
					executableQtyOfAMesChanged = 1
#					printLine("bbb")
				#agg = numpy.delete(agg, (i), axis = 0)
				if(agg[i,1] == 1):
					agg[i,1] = -1
				else:
					agg[i,1] = -2
						
		if(executableQtyOfAMesChanged == 0 and sideIterator >= 2):
			process = 0
		
		else:
			tmp = agg
			agg = contra
			contra = tmp
			sideIterator += 1
	
	return;
		
def checkIfAllQOsFilled(agg):
	for i in range(0, len(agg[:,3])):
		if(agg[i,1] == -1):
			return 0;
		if(agg[i,1] == 1 and agg[i,4] < agg[i,3]):
			return 0;
	return 1;
		
def rearrageArray(arr):
	for i in range(0, len(arr[:,3])):
		if(arr[i,1] == -2):
			arr[i,1] = 0.0;
	return;
	
def execute(agg, contra):
	for i in range(0, len(agg[:,3])):
		for j in range(0, len(contra[:,3])):
			if(agg[i,4] == agg[i,5]):
				break
			exec_size = min (agg[i,4] - agg[i,5], contra[j,4] - contra[j,5])
			agg[i,5] += exec_size
			contra[j,5] += exec_size
			if(exec_size > 0.0):
				printLine("\n\t\t"+agg[i,0] + " - " + contra[j,0] + " : " + str(exec_size))
	
	return;

def printTab(len):

	if(len < 4):
		printFile("\t")
	if(len < 8):
		printFile("\t")
	if(len < 12):
		printFile("\t")
	
		
	return;
def processSheet(sheet, file_name):

	global filename
	filename = file_name

	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(2, sheet.nrows)]
	# Profit !
	printLine ("\n-\tInitial Order Book\n")
	printFile ("\n\t\t+-------------------------------------------+-------------------------------------------+")
	printFile ("\n\t\t|                    BUY                    |                   SELL                    |")
	printFile ("\n\t\t+-------------------------------------------+-------------------------------------------+")
	printFile ("\n\t\t|\tOID\t\tQO\t\tMAQ\t\t\tQTY\t\t\t|\tOID\t\tQO\t\tMAQ\t\t\tQTY\t\t\t|")
	printFile ("\n\t\t+-------------------------------------------+-------------------------------------------+")
	
	print("\n+-------------------------------+-------------------------------+")
	print("|               BUY             |              SELL             |")
	print("+-------------------------------+-------------------------------+")
	
	

	i = 0 
	b_x = -1
	b_y = -1
	b_z = -1
	s_x = -1
	s_y = -1
	s_z = -1
	for x in range(0,len(data)):
			tab = "\t"
			maq_len = len(str(data[x][2]))
			qty_len = len(str(data[x][3]))
			printFile ("\n\t\t|"+tab + str(data[x][0]) + "\t\t" + str(data[x][1]) +"\t\t" + str(data[x][2]))
			
			printTab(maq_len)
			printFile(str(data[x][3]))
			printTab(qty_len)
			
			maq_len = len(str(data[x][6]))
			qty_len = len(str(data[x][7]))
			printFile("|"+tab+ str(data[x][4])+"\t\t" + str(data[x][5])+"\t\t" + str(data[x][6]))
			printTab(maq_len)
			printFile(str(data[x][7]))
			printTab(qty_len)
			printFile("|")
				
			print ( "|  " +str(data[x][0]) + "\t" + str(data[x][1]) +"\t" + str(data[x][2])+"\t" + str(data[x][3])+"\t|  " + str(data[x][4])+"\t" + str(data[x][5])+"\t" + str(data[x][6])+"\t" + str(data[x][7])+"\t|")
			if(str(data[x][1]) == "1.0"):
				b_x = x
			elif(str(data[x][1]) == "0.0"):
				b_z = x
				if(b_y == -1):
					b_y = x
			#else:
				
			if(str(data[x][5]) == "1.0"):
				s_x = x
			if(str(data[x][5]) == "0.0"):
				s_z = x
				if(s_y == -1):
					s_y = x
				
			#else:
				
				
	print(b_x)
	print(b_y)
	print(b_z)
	print(s_x)
	print(s_y)
	print(s_z)
	
	printFile ("\n\t\t+-------------------------------------------+-------------------------------------------+")
	print("+-------------------------------+-------------------------------+")
	
	a = numpy.array(data, dtype=numpy.object)
	buy = a[:, 0:4]
	sell = a[:, 4:]
	# if (b_x == 0 and b_z == 0): 
		# b_x = b_z+1
	# if (b_y == 0): 
		# b_y = b_z+1
	buy_qo = buy[:b_x+1,]
	buy_nqo = buy[b_y:b_z+1,]
	if (s_x == 0 and s_z == 0): 
		s_x = s_z+1
	if (s_y == 0): 
		s_y = s_z+1
	sell_qo = sell[:s_x+1,]
	sell_nqo = sell[s_y:s_z+1,]

#	printLine("\n*****All orders*******\n")
#	printLine(a)
#	printLine("\n*****Buy orders*******\n")
#	printLine(buy)
#	printLine("\n*****Sell orders*******\n")
#	printLine(sell)
	print("\n*****Buy QO orders*******\n")
	print(buy_qo)
	print("\n*****Buy NQO orders*******\n")
	print(buy_nqo)
	print("\n*****Sell QO orders*******\n")
	print(sell_qo)
	print("\n*****Sell NQO orders*******\n")
	print(sell_nqo)

	# printLine ("\n==================================================================\n")
	
	buy_qo_total_qty = buy_qo[:,3].astype('float').sum()
	sell_qo_total_qty = sell_qo[:,3].astype('float').sum()

	buy_nqo_total_qty = buy_nqo[:,3].astype('float').sum()
	buy_nqo_total_maq = buy_nqo[:,2].astype('float').sum()

	sell_nqo_total_qty = sell_nqo[:,3].astype('float').sum()
	sell_nqo_total_maq = sell_nqo[:,2].astype('float').sum()

	buy_total_qty = buy_qo_total_qty + buy_nqo_total_qty
	buy_total_maq = buy_qo_total_qty + buy_nqo_total_maq
	sell_total_qty = sell_qo_total_qty + sell_nqo_total_qty
	sell_total_maq = sell_qo_total_qty + sell_nqo_total_maq

	# printLine("\n*****Total Order counts*******\n")

	# printLine("Total Buy = " + str(buy_total_qty) + "("+str(buy_total_maq) + ")")
	# printLine("Total Sell = " + str(sell_total_qty) + "("+str(sell_total_maq) + ")")

	# printLine("Total Buy QO = " + str(buy_qo_total_qty))
	# printLine("Total Sell QO = " + str(sell_qo_total_qty))

	# printLine("Total Buy NQO = " + str(buy_nqo_total_qty) + "("+str(buy_nqo_total_maq) + ")")
	# printLine("Total Sell NQO = " + str(sell_nqo_total_qty) + "("+str(sell_nqo_total_maq) + ")")


	# if (buy_qo_total_qty <= sell_total_qty and sell_qo_total_qty <= buy_total_qty):
		# printLine( "\nQOs can be fully executed - start from buy side")
	# else:
		# printLine("\nQOs can not be fully executed 2")
		
	z = numpy.zeros((len(buy_qo[:,3]),1))
	buy_qo = numpy.concatenate((buy_qo, z), axis=1)
	z = numpy.zeros((len(buy_nqo[:,3]),1))
	buy_nqo = numpy.concatenate((buy_nqo, z), axis=1)
	z = numpy.zeros((len(sell_qo[:,3]),1))
	sell_qo = numpy.concatenate((sell_qo, z), axis=1)
	z = numpy.zeros((len(sell_nqo[:,3]),1))
	sell_nqo = numpy.concatenate((sell_nqo, z), axis=1)

	# buy_nqo = buy_nqo[buy_nqo[:, 2].argsort()]
	# sell_nqo = sell_nqo[sell_nqo[:, 2].argsort()]

	# buy_nqo = buy_nqo[::-1]
	# sell_nqo = sell_nqo[::-1]

		
	buy_all = numpy.concatenate((buy_qo, buy_nqo), axis=0)
	sell_all = numpy.concatenate((sell_qo, sell_nqo), axis=0)

	#buy_temp = numpy.copy(buy_all)
	#sell_temp = numpy.copy(sell_all)

	if (buy_qo_total_qty > sell_total_qty or sell_qo_total_qty > buy_total_qty):
		printLine("\n\n-\tQO one side total volume is larger than contra total volume... discarding QOs and applying Hill Climb Algo on NQO orders\n")
		if(buy_nqo_total_qty > sell_nqo_total_qty):
			agg = buy_nqo
			contra = sell_nqo
		else:
			agg = sell_nqo
			contra = buy_nqo
		applyApplyHilClimbAlgo(agg, contra)
		buy_all = numpy.concatenate((buy_qo, buy_nqo), axis=0)
		sell_all = numpy.concatenate((sell_qo, sell_nqo), axis=0)
	else:
		buy_nqo = buy_nqo[buy_nqo[:, 3].argsort()]
		sell_nqo = sell_nqo[sell_nqo[:, 3].argsort()]
		
		buy_nqo = buy_nqo[::-1]
		sell_nqo = sell_nqo[::-1]
	
		buy_all = numpy.concatenate((buy_qo, buy_nqo), axis=0)
		sell_all = numpy.concatenate((sell_qo, sell_nqo), axis=0)
	
	#	printLine(buy_all)
	#	printLine(sell_all)
		
		if(buy_total_qty > sell_total_qty):
			agg = buy_all
			contra = sell_all
		else:
			agg = sell_all
			contra = buy_all

		printLine("\n\n-\tApplying Hill Climb Algo on all orders")
		applyTwoPhasesHilClimbAlgo(agg, contra)

		if(checkIfAllQOsFilled(agg) == 1 and checkIfAllQOsFilled(contra) == 1):
			printLine("\n\n-\tQOs can be fully filled\n")
			
		else:
			printLine("\n\n-\tQOs can not be fully filled.. hence applying Hill Climb Algo on NQO orders\n")
			if(buy_nqo_total_qty > sell_nqo_total_qty):
				agg = buy_nqo
				contra = sell_nqo
			else:
				agg = sell_nqo
				contra = buy_nqo
			applyApplyHilClimbAlgo(agg, contra)
			buy_all = numpy.concatenate((buy_qo, buy_nqo), axis=0)
			sell_all = numpy.concatenate((sell_qo, sell_nqo), axis=0)


		
	rearrageArray(buy_all)
	rearrageArray(sell_all)

	z = numpy.zeros((len(buy_all[:,3]),1))
	buy_all = numpy.concatenate((buy_all, z), axis=1)
	z = numpy.zeros((len(sell_all[:,3]),1))
	sell_all = numpy.concatenate((sell_all, z), axis=1)


	printLine("\n-\tExecuting Orders\n")
	execute(buy_all,sell_all)
	#n, agg, res = execute(agg, 0, res, 2)
	#printLine(n)
	#printLine("\n Fill Remainder1")
	#executeRemainder(agg,n-1, res)
	#printLine("\n Fill Remainder2")
	#executeRemainder(agg,0, res)
	# buy_qo, sell_qo = execute(buy_qo, sell_qo, 3, 3)
	# buy_qo, sell_nqo = execute(buy_nqo, sell_qo, 2, 3)
	# buy_nqo, sell_qo = execute(buy_nqo, sell_qo, 3, 3)
	# buy_qo, sell_nqo = execute(buy_nqo, sell_nqo, 3, 3)
	# buy_nqo, sell_qo = execute(buy_qo, sell_nqo, 3, 3)
	# buy_nqo, sell_nqo = execute(buy_nqo, sell_nqo, 2, 2)
	# buy_nqo, sell_nqo = execute(buy_nqo, sell_nqo, 3, 3 )
	
	
	printLine("\n\n-\tOrder Book after the Execution\n")
	
	printFile ("\n\t\t+-------------------------------------------------------------------+")
	printFile ("\n\t\t|                              BUY                                  |")
	printFile ("\n\t\t+-------------------------------------------------------------------+")
	printFile ("\n\t\t|\tOID\t\tQO\t\tMAQ\t\t\tQTY\t\t\tExecutable\tExecuted\t|")
	printFile ("\n\t\t+-------------------------------------------------------------------+")
	printFile("\n")
	
	def printNumpyArray(arr):
		for i in range(0, len(arr[:,3])):
			maq_len = len(str(arr[i,2]))
			qty_len = len(str(arr[i,3]))
			executable_len = len(str(arr[i,4]))
			executed_len = len(str(arr[i,5]))
			printFile ("\t\t|\t" + str(arr[i,0]) + "\t\t" + str(arr[i,1]) +"\t\t" + str(arr[i,2]))
			
			printTab(maq_len)
			printFile(str(arr[i,3]))
			printTab(qty_len)
			printFile(str(arr[i,4]))
			printTab(executable_len)
			printFile(str(arr[i,5]))
			printTab(executed_len)
			printFile("|\n")
			
	#printLine(buy_all)
	#printLine(sell_all)
	
	printNumpyArray(buy_all)
	printFile ("\t\t+-------------------------------------------------------------------+")
	
	printFile ("\n\n\n\t\t+-------------------------------------------------------------------+")
	printFile ("\n\t\t|                              SELL                                 |")
	printFile ("\n\t\t+-------------------------------------------------------------------+")
	printFile ("\n\t\t|\tOID\t\tQO\t\tMAQ\t\t\tQTY\t\t\tExecutable\tExecuted\t|")
	printFile ("\n\t\t+-------------------------------------------------------------------+")
	printFile("\n")
	
	printNumpyArray(sell_all)
	printFile ("\t\t+-------------------------------------------------------------------+")
	
	print("\n-----------BUY--------------\n")
	print(buy_all)
	print("\n-----------SELL--------------\n")
	print(sell_all)
	
	
	buy_exec_qty = buy_all[:,5].astype('float').sum()
	sell_exec_qty = sell_all[:,5].astype('float').sum()
	exec_qty = min( buy_exec_qty, sell_exec_qty)
	imbalance_buy = buy_total_qty - exec_qty
	imbalance_sell = sell_total_qty - exec_qty

	printLine("\n\n-\tTotal Order counts\n")

	printLine("\n\n\t\tTotal Buy Order Qty  =\t" + str(buy_total_qty) + "("+str(buy_total_maq) + ")")
	printLine("\n\t\tTotal Sell Order Qty =\t" + str(sell_total_qty) + "("+str(sell_total_maq) + ")")

	printLine("\n\n\t\tTotal Buy QO Order Qty  =\t" + str(buy_qo_total_qty))
	printLine("\n\t\tTotal Sell QO Order Qty =\t" + str(sell_qo_total_qty))

	printLine("\n\n\t\tTotal Buy NQO Order Qty  =\t" + str(buy_nqo_total_qty) + "("+str(buy_nqo_total_maq) + ")")
	printLine("\n\t\tTotal Sell NQO Order Qty =\t" + str(sell_nqo_total_qty) + "("+str(sell_nqo_total_maq) + ")")

	printLine("\n\n\t\tExecuted Qty   =\t" + str(min(buy_exec_qty, sell_exec_qty)))
	printLine("\n\t\tImbalance Buy  =\t" + str(imbalance_buy))
	printLine("\n\t\tImbalance Sell =\t" + str(imbalance_sell))


	correctlyFilled = 1
	if(checkIfLessThanMaqFilled(buy_all)):
		printLine("\n!!!!!!!Buy side incorrectly filled")
		correctlyFilled = 0
	if(checkIfLessThanMaqFilled(sell_all)):
		printLine("\n!!!!!!!Sell side incorrectly filled")
		correctlyFilled = 0
		
	printLine("\n\n-\tVerifying Execution...........\n")
	
	if(correctlyFilled):
		printLine("\n\t\tGood Algorithm")
	else:
		printLine("\n\t\tBad Algorithm")
	
	isQOFilled = 1
	
	for i in range(0, len( buy_all[:,3])):
		if( buy_all[i, 1] == 1.0 and buy_all[i,4] < buy_all[i,3]):
			isQOFilled = 0.0
			
	for i in range(0, len( sell_all[:,3])):
		if( sell_all[i, 1] == 1.0 and sell_all[i,4] < sell_all[i,3]):
			isQOFilled = 0.0
	
	return isQOFilled, exec_qty;


	


	
