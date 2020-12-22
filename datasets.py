#!/usr/bin/env python
#coding=utf-8

import sys
import time
import common.globalConfig
from datetime import date
from urllib.request import Request, urlopen

import pymysql

def connnectDB():
    db = "stock"
    con = pymysql.connect(host="localhost", port=3306, user="root", password="123456", charset="utf8")
    try:
        print("open db:{}".format(db))
        con.select_db(db)
    except BaseException as err:
        con.cursor().execute("create database {}".format(db))
        con.select_db(db)
    return con

def insertData(con:pymysql.connect, kLineData:list, table: object)->bool:
    dateStr = "\"{}\"".format(kLineData[0])
    try:
        con.cursor().execute("insert into {} (date,start,end,max,min,volume,quota,amplitude,roc, voc,tor) value({},{},{},{},{},{},{},{},{},{},{});".format(table, dateStr, kLineData[1], kLineData[2], kLineData[3], kLineData[4], kLineData[5], kLineData[6],kLineData[7],kLineData[8],kLineData[9],kLineData[10]))
        return True
    except Exception as err:
        return False

# 这个地址也能拉到数据
# http://qt.gtimg.cn/q=sh600031
def getKLineDayUrl(prev, id, begin, t)->str:
    return "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124009517967901227564_1597003341751&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid={}.{}&beg={}&end=20500000&_={}".format(prev, id, begin, t)

def getData(code, valueType, begin)->str:
    t = int(time.time() * 1000)
    codeHead = code[:1]
    url = ""
    if code == "000001" and valueType == "z":
        if valueType == "z":
            url = getKLineDayUrl(1, code, begin, t)
        else:
            url = getKLineDayUrl(0, code, begin, t)
    elif codeHead == "6":
        url = getKLineDayUrl(1, code, begin, t)
    elif codeHead == "0":
        url = getKLineDayUrl(0, code, begin, t)
    elif codeHead == "3":
        url = getKLineDayUrl(0, code, begin, t)
    elif codeHead == "7":
        url = getKLineDayUrl(1, code, begin, t)
    else:
        url = getKLineDayUrl(1, code, begin, t)
    # req = Request(url)
    respones = None
    try:
        respones = urlopen(url)
    except Exception as err:
        print("err:{}".format(err))
        return "", err
    data = respones.read()
    # print(data)
    return str(data), None

def createTable(con:pymysql.connect, code:str, valueType:str):
    print("handle:{}".format(code))
    sor = con.cursor()
    tableName = "{}_{}".format(valueType, code)
    isNew = False
    # check table is exist
    try:
        sor.execute('''select *from {} order by date desc limit 1;'''.format(tableName))
    except Exception:
        isNew = True

    # create begin param
    begin = "0"
    if not isNew:
        data = sor.fetchall()
        # 没数据，从头取
        # 有数据，就从最后一条向后取
        if len(data) > 0:
            d = data[0][0]
            begin = "{}{}{}".format(d.year, str(d.month).zfill(2), str(d.day).zfill(2))

    # get origin data
    resp, err = getData(code, valueType, begin)
    if err != None:
        return err

    # calculate str kline begin index
    klinesIndex = 0
    try:
        klinesIndex = resp.index("klines")
    except Exception:
        print("no data.code:{}".format(code))
        return

    # if table is not exit, and this code has kline data, then create table
    if isNew:
        # create new table
        sor.execute('''create table {} (
                date date primary key comment 'date',
                start float comment 'start',
                end float comment 'end',
                max float comment 'max',
                min float comment 'min',
                volume int comment 'volume',
                quota float comment 'quota',
                amplitude float comment 'amplitude',
                roc float comment 'range of change',
                voc float comment 'value of change',
                tor float comment 'turnover rate'
            )'''.format(tableName))
    # print(klinesIndex)
    # cut origin string for klinedata string
    resp = resp[klinesIndex + 10:-8]
    # print(resp)
    klineDatas = resp.split("\",\"")
    for i in range(len(klineDatas)):
        info = klineDatas[i]
        klineDatas[i] = info.split(",")
    n = 0
    for kLineData in klineDatas:
        if insertData(con, kLineData, tableName):
            n = n + 1
    print("insert {} row".format(n))
    con.commit()

print("start! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))

con = connnectDB()
# createTable(con, "300015")
# createTable(con, "601001")
# createTable(con, "002001")
# createTable(con, "000300")

heads = common.globalConfig.heads
blacklist = common.globalConfig.blackList
for head in heads:
    for i in range(0, 1000):
        code = "{}{}".format(head, str(i).zfill(3))
        if not code in blacklist:
            err = createTable(con, code, "s")
            if err != None:
                print(err)
            
createTable(con, "000001", "z")
createTable(con, "399001", "z")
createTable(con, "399006", "z")

con.close()

print("over! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))
sys.exit()

