# VCF-to-23andMe
These scripts convert an imputed DNA.Land VCF into the 23andMe V3 raw data format.

Firstly, vcf_to_db.py converts the VCF file into an indexed SQLite3 database for quick searching. db_to_23.py then inserts genotypes into the blank V3 file retrieved from the database by chromosome, position and identifier.

##Requirements
* Python3

##Usage
```
python3 vcf_to_db.py <INPUT_VCF> <OUTPUT_DB>
python3 db_to_23.py <INPUT_DB> <INPUT_BLANK_23_RAW> <OUTPUT_23_RAW>
```

##Usage Example
```
python3 vcf_to_db.py imputed.vcf imputed.vcf.db
python3 db_to_23.py imputed.vcf.db blank_v3.txt genome_Fred_Bloggs_Full_20140628012345.txt
```
