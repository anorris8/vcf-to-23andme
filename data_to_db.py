#!/usr/bin/env python3
# Copyright (c) 2015-2016 Sean Hewitt <contact@SeanHewitt.com>
# Licensed under the MIT license: http://SeanHewitt.com/MIT-LICENSE.txt

import sys, io
import gzip, zipfile
import csv, sqlite3

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

def open_file(file_name):
	data_file = gzip.open(file_name, "rt", encoding="utf8")
	try:
		data_file.read(1);
	except OSError:
		data_file.close()
	else:
		data_file.seek(0);
		return data_file
		
	try:
		archive = zipfile.ZipFile(file_name)
	except zipfile.BadZipFile:
		pass
	else:
		for object_name in archive.namelist():
			if not object_name.endswith("/"):
				break
		else:
			raise Exception("ZIP Archive has no readable file")
		
		data_file = io.TextIOWrapper(archive.open(object_name), encoding="utf8")
		archive.close()
		return data_file
		
	return open(file_name, "r", encoding="utf8")

try:
	data_file = open_file(data_file_name)
except Exception as e:
	print(e)
	exit()

reader = csv.reader(data_file, delimiter="\t", quoting=csv.QUOTE_NONE)
print("Processing " + data_format + " data file...")
for i, line in enumerate(reader):
	if not line or line[0].startswith("#"):
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

print("Lines read:", i+1)

data_file.close()

conn.commit()
conn.close()
