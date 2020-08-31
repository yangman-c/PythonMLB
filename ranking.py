import sys
import time

import numpy as np
import pymysql

z_000001 = None
z_399001 = None
z_399006 = None
numOfCode = dict()

class TestInfo(object):
    def __init__(self, code, varm, roc, mean, tor):
        self.varm = varm
        self.roc = roc
        self.code = code
        self.mean = mean
        self.tor = tor
    def __str__(self):
        return "[TestInfo code:{} varm:{} roc:{} mean:{} tor:{}]".format(self.code, self.varm, self.roc , self.mean, self.tor)


def readDB(con:pymysql.connect, tableName, n)->(Exception, TestInfo):
    cursor = con.cursor()
    length = 0
    try:
        length = cursor.execute('''select end,tor from {} order by date desc limit 0,{};'''.format(tableName, n))
        # print("length:{}".format(length))
    except Exception as err:
        # print("select err:{}".format(err))
        return err, None
    allData = np.array(cursor.fetchall())
    cursor.close()
    if len(allData) == 0:
        return None, None
    roc = ((allData[0][0] / allData[-1][0]) - 1) * 100
    endInfo = allData[:,0]
    tor = allData[:,1].mean()
    var = endInfo.var()
    mean = endInfo.mean()
    info = TestInfo(tableName[2:], var / mean / n, roc, endInfo.mean(), tor)
    return None, info

def connectDB()->pymysql.connect:
    con = pymysql.connect(host="localhost", port=3306,user="root",password="123456")
    try:
        # print("open db")
        con.select_db("stock")
    except Exception:
        print("can not find db:stock")
        con.close()
        sys.exit()
    return con

def getZSByCode(code):
    head = code[0]
    if head == "6":
        return z_000001
    elif head == "0":
        return z_399001
    elif head == "3":
        return z_399006
    else:
        return z_000001

def makeRanking(n, con):
    print("\n==================== start n={} ====================".format(n))
    global z_000001, z_399001, z_399006
    err, z_000001 = readDB(con, "z_000001", n)
    err, z_399001 = readDB(con, "z_399001", n)
    err, z_399006 = readDB(con, "z_399006", n)
    print(z_000001)
    print(z_399001)
    print(z_399006)

    allData = list([])
    heads = ("000", "002", "300", "600", "601", "603")
    for head in heads:
        for i in range(1000):
            code = "{}{}".format(head, str(i).zfill(3))
            err, info = readDB(con, "s_{}".format(code), n)
            if err == None and info != None and info.roc >= getZSByCode(info.code).roc:
                if info.code in numOfCode:
                    numOfCode[info.code] = numOfCode[info.code] + 1
                else:
                    numOfCode[info.code] = 1
                allData.append(info)

    # allData = filter(lambda TestInfo:TestInfo.roc > getZSByCode(TestInfo.code).roc, allData)
    rocsort = sorted(allData, key=lambda TestInfo:TestInfo.roc, reverse=True)
    for info in rocsort:
        print(info)
    print("==================== end n:{} total:{} ====================\n".format(n, len(rocsort)))
    return rocsort

def main():
    print("start! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))
    con = connectDB()
    makeRanking(5, con)
    makeRanking(10, con)
    makeRanking(15, con)
    makeRanking(20, con)
    makeRanking(25, con)
    makeRanking(30, con)
    makeRanking(35, con)
    makeRanking(40, con)
    makeRanking(45, con)
    makeRanking(50, con)
    makeRanking(55, con)
    makeRanking(60, con)
    makeRanking(100, con)
    makeRanking(200, con)
    makeRanking(300, con)

    items = list(numOfCode.items())
    items.sort(key=lambda x:x[1], reverse=True)
    for item in items:
        print("code:{} num:{}".format(item[0], item[1]))
    print("over! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))
    return

main()
sys.exit()