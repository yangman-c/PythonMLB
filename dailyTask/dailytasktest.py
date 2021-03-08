import pymysql
import numpy as np
import sys
import os
from datetime import date
import time
from eastmoney.commonInterface import getKLineDayUrl

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

def readDB(con:pymysql.connect, tableName, n)->(date, Exception):
    cursor = con.cursor()
    length = 0
    try:
        length = cursor.execute(f"select date from {tableName} order by date desc limit 0,{n};")
        # print("length:{}".format(length))
    except Exception as err:
        # print("select err:{}".format(err))
        return "", err
    allData = np.array(cursor.fetchall())
    cursor.close()
    if len(allData) == 0:
        return "", ""
    return allData[0], None

con = connectDB()
# 数据库最新
info, err = readDB(con, "s_000001", 1)
print(info)

t = int(time.time() * 1000)
response, err = getKLineDayUrl(1, "000001", time.strftime("%Y%m%d"), t)
dateStr:str = response['data']['klines'][0][0:10]
year = int(dateStr[0:4])
month = int(dateStr[5:7])
day = int(dateStr[8:10])
# 当前最新
d = date(year=year, month = month, day=day)

# 如果当前的比数据库的新，就需要处理
if d > info:
    os.system("maintask.bat")
else:
    print(f"no task newD:{d} curD:{info}")

if __name__ == '__main__':
    sys.exit()