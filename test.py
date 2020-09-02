import math
import os
import sys
import openpyxl
from openpyxl.worksheet import worksheet

mywb = openpyxl.Workbook()
mysheet = mywb.active
mysheet['F6'] = 500
mysheet['F7'] = 800
mysheet['AD3'] = '=SUM(F6:F7)'
sheet = mywb.create_sheet("testsheet")
# sheet.append({1 : 'This is A1', 3 : 'This is C1'})
mywb.save('Applyingformula.xlsx')



def getname(i):
    colName = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    l = []
    length = len(colName)
    while True:
        m = i % length
        i = math.floor(i / length)
        if m == 0:
            m = length
            i = i - 1
        l.append(m)
        if i == 0:
            break
    name = ""
    for c in l:
        name = colName[c-1] + name
    return name

# for i in range(1,1000):
#     print("i:{} name:{}".format(i,getname(i)))

sys.exit()