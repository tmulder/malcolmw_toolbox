#! /opt/antelope/5.2-64/bin/python

#catalogue_subset -s -p dbin dbout
#  send dbout to orb, email, etc.

import sys
import os
import getopt

import antelope.datascope as datascope
import antelope.stock as stock

##################
### START MAIN ###
##################
def main():
	if len(sys.argv) < 3:
		print ('usage: ' + sys.argv[0] + '[-s] [-p] input_db output_db')
		exit()

	pf = os.path.splitext(sys.argv[0])[0] #use program name (argv[0]) as pf name by default

	optlist,args = getopt.getopt(sys.argv[1:], 's:p:')

	for opt,arg in optlist:
		if opt == '-p':
			pf = arg

	subset_expression = stock.pfget_string(pf, 'subset_expression')

	table_list = list(stock.pfget_tbl(pf, 'table_list'))

	for opt,arg in optlist:
		if opt == '-s':
			subset_expression = arg

	dbin = datascope.dbopen(args[0], 'r')#die gracefully if dbin doesn't exist

	if os.path.isfile(args[1]) == False:
		datascope.dbcreate(args[1],'css3.0')
		print 'Output database created: ' + args[1]

	dbout = datascope.dbopen(args[1],'r+')

	dbin = dbin.lookup(table=table_list[0])

	for a_table in table_list[1:]:
		dbin = dbin.join(dbin.lookup(table=a_table), outer=False)

	dbin = dbin.subset(subset_expression)

	copy_missing_records(dbin, dbout, table_list)

	dbin.close()
	dbout.close()
		

################
### END MAIN ###
################

##########################
### START SUB-ROUTINES ###
##########################

def get_row(dbin):
	fields = dbin.query(datascope.dbTABLE_FIELDS)

	record = []

	for a_field in fields:
		record.append((a_field, dbin.getv(a_field)[0]))

	return record



def put_row(dbout, record, put_table):
	put_table_ptr = dbout.lookup(table = put_table)

	primary_keys = list(put_table_ptr.query(datascope.dbPRIMARY_KEY))

	primary_key_index_pairs = get_primary_key_index_pairs(primary_keys, record)

	num_keys = len(primary_key_index_pairs)

	if num_keys == 1:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to table ' + put_table
	elif num_keys == 2:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], primary_key_index_pairs[1][0], record[primary_key_index_pairs[1][1]][1], table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to ' + put_table

	elif num_keys == 3:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], primary_key_index_pairs[1][0], record[primary_key_index_pairs[1][1]][1], primary_key_index_pairs[2][0], record[primary_key_index_pairs[2][1]][1], table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to ' + put_table

	elif num_keys == 4:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], primary_key_index_pairs[1][0], record[primary_key_index_pairs[1][1]][1], primary_key_index_pairs[2][0], record[primary_key_index_pairs[2][1]][1], primary_key_index_pairs[3][0], record[primary_key_index_pairs[3][1]][1], table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to ' + put_table

	elif num_keys == 5:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], primary_key_index_pairs[1][0], record[primary_key_index_pairs[1][1]][1], primary_key_index_pairs[2][0], record[primary_key_index_pairs[2][1]][1], primary_key_index_pairs[3][0], record[primary_key_index_pairs[3][1]][1], primary_key_index_pairs[4][0], record[primary_key_index_pairs[4][1]][1], table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to ' + put_table

	elif num_keys == 6:
		dbout[3] = dbout.addv(primary_key_index_pairs[0][0], record[primary_key_index_pairs[0][1]][1], primary_key_index_pairs[1][0], record[primary_key_index_pairs[1][1]][1], primary_key_index_pairs[2][0], record[primary_key_index_pairs[2][1]][1], primary_key_index_pairs[3][0], record[primary_key_index_pairs[3][1]][1], primary_key_index_pairs[4][0], record[primary_key_index_pairs[4][1]][1], primary_key_index_pairs[5][0], record[primary_key_index_pairs[5][1]][1],table=put_table)
		if dbout[3] < 0:
			print 'dbout.addv() failed adding primary keys to ' + put_table

	else:
		print 'Number of primary keys in ' + put_table + ' table is equal to 0 or greater than 6 - case not handled, alter put_row() function'
		exit()

	for i in range(len(record)):
		if dbout.putv(record[i][0], record[i][1], table=put_table) < 0:
			print 'dbout.putv() failed adding field ' + record[i][0] + ' to table ' + put_table
			#print str(i) + '\t' + 'put_table: ' + put_table + '\t record length: ' + str(len(record)) + '\t' + str(dbout)

def get_primary_key_index_pairs(primary_keys, record):
	primary_key_index_pairs = []

	for i in range(len(primary_keys)):
		for j in range(len(record)):
			if record[j][0] == primary_keys[i]:
				primary_key_index_pairs.append((primary_keys[i],j))

	return primary_key_index_pairs

def copy_missing_records(dbin, dbout, table_list):
	for i in range(dbin.nrecs()):
		dbin[3] = i

		orid = dbin.getv('orid')[0]

		dbout = dbout.lookup(table='origin')

		if dbout.find('orid == ' + str(orid)) < 0:
			print 'copying data for orid: ' + str(orid)
			copy_subset = dbin.subset('orid == ' + str(orid))
			
			#copy origin table
			copy_table = copy_subset.separate('origin')
			copy_table[3] = 0

			dbout = dbout.lookup(table='origin')

			put_row(dbout, get_row(copy_table), 'origin')
			
			copy_table.free()

			#for each other table, copy table
			for a_table in table_list:
				if a_table != 'origin':
					copy_table = copy_subset.separate(a_table)

					dbout = dbout.lookup(table=a_table)

					for i in range(copy_table.nrecs()):
						copy_table[3] = i
						put_row(dbout, get_row(copy_table), a_table)

					copy_table.free()			

########################
### END SUB-ROUTINES ###
########################

main()