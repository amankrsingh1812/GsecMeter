import json
import sys
import os
import xlrd
import json
# from gsecWorkStatus.models import agenda
# from django.db import models
# from gsecWorkStatus.models import agenda


# agenda_count=agenda.objects.all().count()

# number=views.agenda_count()

base= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# can be made dyanamic
filename=input("enter name of xlsx sheet : ")

# filename=

# json_file_name=
file_location=os.path.join(base, "gsecWorkStatus/fixtures",filename+'.xlsx')
json_file_name=input("enter json file name")

json_file=os.path.join(base, "gsecWorkStatus/fixtures",json_file_name+'.json')
workbook = xlrd.open_workbook(file_location)
sheetnumber=int(input("enter sheet number(counting starts from 0 : "))
sheet = workbook.sheet_by_index(sheetnumber)
value=sheet.cell_value(0,0)
# print(value)
agenda_list=[]
agenda_dict={  "model": "gsecWorkStatus.agenda","pk": 0}
heading_list=[]

number =int(input("maximum pk value till now of mode agenda : "))

# print(number)
for col in range(sheet.ncols):
    value=sheet.cell_value(0,col)
    heading_list.append(value)

# print(heading_list)
agenda_detail_dict= {}
a=[]
for row in range(1,sheet.nrows):
    for col in range(sheet.ncols):
        value=sheet.cell_value(row,col)
        agenda_detail_dict[heading_list[col]]=value
    # print(agenda_detail_dict)
    agenda_dict['fields']=agenda_detail_dict.copy()
    agenda_dict['pk'] = row+number
    agenda_list.append(agenda_dict.copy())
    # print(agenda_dict)

print(agenda_list)

fout = open(json_file,'w')
json.dump(agenda_list,fout, indent=2)
fout.close()


