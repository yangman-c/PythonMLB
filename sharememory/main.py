import sys
import common.globalConfig
import numpy as np
from multiprocessing.shared_memory import SharedMemory

import pymysql

shmlist = list([])

def makeShm(name, arr, dtype):
    try:
        sm = SharedMemory(name, True, arr.nbytes)
    except Exception as err:
        print("makeShm err:{}".format(err))
        return
    print("makeShm:{} size:{}".format(name, arr.nbytes))
    b = np.ndarray(arr.shape, dtype=dtype, buffer=sm.buf)
    b[:] = arr[:]
    shmlist.append(sm)
    return

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

def readZS(con:pymysql.connect):
    cursor = con.cursor()
    try:
        cursor.execute('''select *from z_000001''')
        z_000001 = list(cursor.fetchall())
        cursor.execute('''select *from z_399001''')
        z_399001 = list(cursor.fetchall())
        cursor.execute('''select *from z_399006''')
        z_399006 = list(cursor.fetchall())
    except Exception as err:
        print("select err:{}".format(err))
    maxLen = 0
    for data in [z_000001, z_399001, z_399006]:
        length = len(data)
        if length > maxLen:
            maxLen = length
        for i in range(length):
            elem = list(data[i])
            d = elem[0]
            data[i] = [d.year, d.month, d.day] + elem[1:]
    # 数据长度不等，使用最长的数据给别的数据补齐
    z_000001 = data[:maxLen-len(z_000001)] + z_000001
    z_399001 = data[:maxLen-len(z_399001)] + z_399001
    z_399006 = data[:maxLen-len(z_399006)] + z_399006
    return

def readDB(con:pymysql.connect, tableName):
    cursor = con.cursor()
    length = 0
    try:
        length = cursor.execute('''select *from {} ;'''.format(tableName))
        # print("length:{}".format(length))
    except Exception as err:
        print("select err:{}".format(err))
        return
    allData = list(cursor.fetchall())
    # 把索引1的数据(date)按照年月日展开
    for i in range(0, len(allData)):
        data = list(allData[i])
        d = data[0]
        data = [d.year, d.month, d.day] + data[1:]
        allData[i] = data
    cursor.close()
    arr = np.array(allData)
    makeShm(tableName, arr, np.float)
    makeShm(tableName + "_shape", np.array(arr.shape), np.int)
    return allData

def main():
    con = connectDB()
    heads = common.globalConfig.heads
    for head in heads:
        for i in range(1000):
            code = "{}{}".format(head, str(i).zfill(3))
            readDB(con, "s_{}".format(code))

    readDB(con, "z_000001")
    readDB(con, "z_399001")
    readDB(con, "z_399006")
    return


main()
print("start main")
