#!/usr/bin/python

import sys
import csv

COL_TABLE_NAME = 6
COL_CONSTRAINT_NAME = 11
COL_FK_FIELD = 7

if len(sys.argv) != 3:
    print("Invalid arguments!")
    print("Usage:")
    print(" $py sql-constraints.py [CONSTRAINTSFILE.CSV] [FOREIGN-TABLE-NAME")
    sys.exit()

foreign_table_name = sys.argv[2]

try:
    file_constraints = open(sys.argv[1], mode='r')
except IOError as e:
    print(f"Could not open file {sys.argv[1]}\n{str(e)}")
    sys.exit()

try:
    file_drop = open("out\\drop_constraints.sql", mode='w')
except IOError as e:
    print(f"Could not open file drop_constraints.sql for writing\n{str(e)}")
    file_constraints.close()
    sys.exit()


try:
    file_recreate = open("out\\recreate_constraints.sql", mode='w')
except IOError as e:
    print(
        f"Could not open file recreate_constraints.sql for writing\n{str(e)}")
    file_constraints.close()
    file_drop.close()
    sys.exit()

csv_reader = csv.reader(file_constraints, delimiter=';')
for row in csv_reader:
    file_drop.write(
        f'ALTER TABLE {row[COL_TABLE_NAME]} DROP CONSTRAINT {row[COL_CONSTRAINT_NAME]}\n')
    file_recreate.write(
        f'ALTER TABLE {row[COL_TABLE_NAME]} WITH NOCHECK ADD  CONSTRAINT [{row[COL_CONSTRAINT_NAME]}] FOREIGN KEY([{row[COL_FK_FIELD]}]) REFERENCES [dbo].[{foreign_table_name}] ([ID])\n')
    file_recreate.write(
        f'ALTER TABLE {row[COL_TABLE_NAME]} CHECK CONSTRAINT {row[COL_CONSTRAINT_NAME]}\n')

file_recreate.close()
file_drop.close()
file_constraints.close()

print('Done!')
