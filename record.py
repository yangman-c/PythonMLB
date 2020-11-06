import sys
import re
import openpyxl
import os
import common.globalConfig

class RecordInfo(object):
    def __init__(self, code):
        self.code = code
        self.totalTimes = 0
        self.totalRecord = 0
        return
    def addRecord(self, record):
        self.totalRecord += record
        self.totalTimes += 1
    def getRecord(self):
        return self.totalRecord / self.totalTimes
    def getTotalTimes(self):
        return self.totalTimes

def main():
    path = "ranking/"
    fileList = os.listdir(path)
    i = 0
    dic = dict()
    for fileName in fileList:
        if re.match("Ranking_\d{4}-\d{2}-\d{2}\.xlsx", fileName) == None:
            continue
        print("read file:{}".format(fileName))
        i += 1
        wb = openpyxl.open(path + fileName)
        for row in wb.active.rows:
            code = row[0].value
            if code == "Code":
                continue
            if code in common.globalConfig.blackList:
                continue
            record = 0
            for j in range(1,len(list(row)) - 1):
                if row[j].value == 1:
                    record += 1
            if code in dic:
                pass
            else:
                dic[code] = RecordInfo(code)
            dic[code].addRecord(record)

    wb = openpyxl.Workbook()
    wb.active.title = "{}日得分".format(i)
    wb.active.append(("Code", "Record", "Times"))
    for (key, recordInfo) in dic.items():
        print(key, recordInfo.getRecord())
        wb.active.append((str(key), recordInfo.getRecord(), recordInfo.getTotalTimes()))
    wb.save(path + "record.xlsx")
    return

print("record start.")
main()
print("record over.")
sys.exit()