#!/usr/bin/env python3

import sqlite3
from sys import argv

_, vcf_file_name, db_file_name = argv

conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

cursor.execute('''create table genome
(
	chromosome text,
	position int,
	identifier text,
	reference_base text,
	alternative_base text,
	quality int,
	filter text,
	info text,
	format text,
	data text
)''')

insert_statement = "insert into genome values (?,?,?,?,?,?,?,?,?,?)"

for line in open(vcf_file_name, "r"):
	if line.startswith("#"):
		continue
	line = line.strip()
	try:
		line = line.split("\t")
	except:
		continue
	
	cursor.execute(insert_statement, line)

cursor.execute("create index genome_position_index on genome (chromosome, position)")

conn.commit()
conn.close()
