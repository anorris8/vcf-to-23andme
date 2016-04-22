#!/usr/bin/env python

import sys
import csv
import sqlite3
from sys import argv

csv.field_size_limit(sys.maxsize)

_, data_file_name, data_format, db_file_name = argv

conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

cursor.execute('''create table if not exists
	genome
(
	chromosome text,
	position int,
	identifier text,
	genotype text
)''')
cursor.execute('''create unique index if not exists
	genome_unique_index
on
	genome
(
	chromosome,
	position,
	identifier
)''')

insert_statement = "insert or replace into genome values (?,?,?,?)"

with open(data_file_name, "r") as data_file:
	reader = csv.reader(data_file, delimiter="\t", quoting=csv.QUOTE_NONE)
	for i, line in enumerate(reader):
		if line[0].startswith("#"):
			continue
		
		if data_format == "vcf":
			if len(line) < 10 or line[0][0] == "<":
				continue
			try:
				gt_data_index = line[8].split(":").index("GT")
			except:
				continue
			
			bases = [line[3]] + line[4].split(",")
			
			genotype = ""
			base_indexes = line[9].split(":")[gt_data_index].replace("|", "/").split("/")
			valid = False
			for base_index in base_indexes:
				if base_index == ".":
					break
				base = bases[int(base_index)]
				if len(base) > 1:
					break
				genotype += base[0]
			else:
				valid = True
			
			if not valid:
				continue
				
			row = line[:3]
			row.append(genotype)
			
		elif data_format == "23andme":
			if len(line) < 4:
				continue
			row = (line[1], line[2], line[0], line[3])
			
		else:
			print("Unknown data format: " + data_format)
			exit()
		
		cursor.execute(insert_statement, row)

print("Lines:", i)

conn.commit()
conn.close()
