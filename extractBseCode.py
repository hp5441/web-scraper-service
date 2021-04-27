import csv
import json

temp = {}

with open("Select.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count=0
    for row in csv_reader:
        temp_dict={}
        if row[4]=="Active" and row[9]=="Equity":
            temp_dict['security-bse-code'] = row[0].strip()
            temp_dict['security-name'] = row[3].strip()
            temp_dict['security-group'] = row[5].strip()
            temp_dict['security-fv'] = row[6].strip()
            temp_dict['security-isin'] = row[7].strip()
            temp_dict['security-industry'] = row[8].strip()
            temp[row[2]] = temp_dict

with open("bselist.json","w") as output:
    json.dump(temp, output, indent=4)
        

