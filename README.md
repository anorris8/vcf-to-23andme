# VCF-to-23andMe
These scripts convert an imputed DNA.Land VCF into the 23andMe V3 raw data format.

data_to_db.py is used to convert the VCF file and any additional 23andMe raw data file (adds 23andMe indentifiers) into an indexed SQLite3 database for quick searching. db_to_23.py then inserts genotypes into the blank V3 file retrieved from the database by chromosome, position and identifier.

The data_to_db.py script accepts both compressed and uncompressed data files.

## Requirements
* Python3

## Usage
```
python data_to_db.py <INPUT_VCF> vcf <OUTPUT_DB>
python data_to_db.py <INPUT_23_RAW> 23andme <OUTPUT_DB>
python db_to_23.py <INPUT_DB> <INPUT_BLANK_23_RAW> <OUTPUT_23_RAW>
```

## Usage Example
```
python data_to_db.py imputed.vcf.gz vcf genome.db
python data_to_db.py genome_Fred_Bloggs_v4_Full_20160423012345.zip 23andme genome.db
python db_to_23.py genome.db blank_v3.txt genome_Fred_Bloggs_Full_20140628012345.txt
```
