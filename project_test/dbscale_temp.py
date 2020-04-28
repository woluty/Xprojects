#!/usr/bin/env python
import re

table_count_pattern = re.compile(r"^\| +([0-9]+)")
xx=[]
xx.append()
i = 10000
row_lines = {}
lines = [line.lstrip().rstrip() for line in open('temp_0117.txt')]
for line in lines:
    if 'select count(*)' in line:
        i += 1
        table_name = str(i)+"_"+line.split()[3]
    elif table_count_pattern.match(line) :
        table_count_value = table_count_pattern.findall(line)[0]
        row_lines[table_name] = table_count_value
        continue
    else:
        continue
for table_name in row_lines.keys():
    print(table_name+":"+row_lines[table_name])