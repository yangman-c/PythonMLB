import math

import openpyxl

class RankingXls(object):
    def __init__(self):
        self.xls = openpyxl.Workbook()
        self.maxMainSheetRow = 1
        self.code2RowDic = dict()
        self.xls.active.title = "avrange of n"
        self.mainSheet = self.xls.active
        self.xls.active["A1"] = "Code"
        return

    def setCodeN(self, code, i, value):
        if code in self.code2RowDic:
            pass
        else:
            self.maxMainSheetRow = self.maxMainSheetRow + 1
            self.code2RowDic[code] = self.maxMainSheetRow
            self.mainSheet['A{}'.format(self.maxMainSheetRow)] = code
        colName = self.getname(i)
        self.mainSheet["{}{}".format(colName, self.code2RowDic[code])] = value
        return

    def getAvrangeSheet(self, n):
        title = "{}日".format(n)
        if title in self.xls:
            return self.xls[title]
        else:
            sheet = self.xls.create_sheet(title)
            sheet.append(("Code", "Varm", "Roc", "Mean", "Tor"))
            return sheet

    def getname(self, i):
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

    def save(self, path):
        try:
            self.xls.save(path)
        except Exception as err:
            print("save err:{}".format(err))
        return