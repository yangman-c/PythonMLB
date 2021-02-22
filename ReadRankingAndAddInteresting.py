import sys
import openpyxl
from common.globalConfig import blackList
from eastmoney.EastMoneyController import EastMoneyController
from eastmoney.eastmoneycookies import allCooies

def addInteresting(readFile, recordLine, newGroup):
    print(f"readFile:{readFile} recordLine:{recordLine} newGroup:{newGroup}")
    try:
        wb = openpyxl.open(readFile)
    except Exception as err:
        print(err)
        sys.exit()

    ctls = []
    for cookie in allCooies:
        ctl = EastMoneyController(cookie)
        ctls.append(ctl)
        if newGroup == "y":
            groupName = readFile[readFile.index("Ranking_") + len("Ranking_"):]
            groupName = groupName.replace(".xlsx", "").replace("-", "")
            ctl.checkAndCreateNewGroup(groupName)

    for row in wb.active.rows:
        code = row[0].value
        # 删除第一行
        if code == "Code":
            continue
        if code in blackList:
            continue
        record = 0
        for j in range(1,len(list(row)) - 1):
            if row[j].value == 1:
                record += 1

        if record >= int(recordLine):
            for ctl in ctls:
                ctl.addNewCode(code)

    print("addInteresting ok")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("参数必须是3个")
        sys.exit()
    readFile = sys.argv[1]
    # 目前满分是60
    recordLine = sys.argv[2]
    newGroup = sys.argv[3]
    addInteresting(readFile, recordLine, newGroup)
    sys.exit()
