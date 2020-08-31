import openpyxl

class RankingXls(object):
    def __init__(self):
        self.xls = openpyxl.Workbook()
        self.maxMainSheetRow = 0
        self.code2RowDic = dict()
        self.maxMainSheetColumn = 0
        self.n2ColumnDic = dict()
        self.xls.active.title = "avrange of n"
        self.mainSheet = self.xls.active
        self.xls.active["A1"] = "Code"
        return

    def getSheet(self, n):
        sheetName = "{}日".format(n)
        if sheetName in self.xls:
            return self.xls[sheetName]
        else:
            return self.xls.create_sheet("{}日".format(n))

    def setCodeN(self, code, n):
        if code in self.code2RowDic:
            pass
        else:
            self.maxMainSheetRow = self.maxMainSheetRow + 1
            self.code2RowDic[code] = self.maxMainSheetRow
            self.mainSheet['A' + self.maxMainSheetRow] = code

        if n in self.n2ColumnDic:
            pass
        else:
            self.maxMainSheetColumn = self.maxMainSheetColumn + 1
            self.n2ColumnDic[n] = self.maxMainSheetColumn
            self.mainSheet['B' + 1] = n + "日"

        r = self.code2RowDic[code]
        l = self.n2ColumnDic[n]
        return

    def createColumn(self):
        return

    def save(self):
        self.xls.save("Ranking.xlsx")
        return