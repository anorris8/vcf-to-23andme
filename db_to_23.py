#!/usr/bin/env python3

import sqlite3
from sys import argv

_, db_file_name, blank_file_name, output_file_name = argv

conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

output_file = open(output_file_name, "w")


for i, line in enumerate(open(blank_file_name, "r")):
	if i != 0:
		output_file.write("\r\n")
	if line == "":
		break
		
	line = line.rstrip()
	output_file.write(line)
	
	if line.startswith("#"):
		continue
	
	try:
		identifier, chromosome, position = line.split("\t")[:3]
	except:
		continue
	
	cursor.execute('''select
	reference_base,
	alternative_base,
	data,
	identifier
from
	genome
where
	chromosome = ? and
	position = ? and
	identifier=?
''', (chromosome, int(position), identifier))
	
	row = cursor.fetchone()
	
	if row is None:
		output_file.write("\t--")
		continue
	reference_base, alternative_base, data, other_identifier = row
	
	gt = data.split(":")[0].split("/")
	genotype = (reference_base[0], alternative_base[0])[int(gt[0])]
	if chromosome != "X":
		genotype += (reference_base[0], alternative_base[0])[int(gt[1])]
	
	output_file.write("\t" + genotype)

output_file.write("\r\n")
output_file.close()
