import os
import sys
import openpyxl
from openpyxl.worksheet import worksheet

mywb = openpyxl.Workbook()
mysheet = mywb.active
mysheet['F6'] = 500
mysheet['F7'] = 800
mysheet['D3'] = '=SUM(F6:F7)'
mywb.create_sheet("testsheet")
mywb.save('Applyingformula.xlsx')

sys.exit()