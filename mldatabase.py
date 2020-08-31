import sys
import time

import pymysql
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import  train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor



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

z_000001 = []
z_399001 = []
z_399006 = []
def readZS(con:pymysql.connect):
    cursor = con.cursor()
    global z_000001, z_399001, z_399006
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


def readDB(con:pymysql.connect, id):
    cursor = con.cursor()
    length = 0
    try:
        length = cursor.execute('''select *from s_{} ;'''.format(id))
        # print("length:{}".format(length))
    except Exception as err:
        print("select err:{}".format(err))
        sys.exit()
    allData = list(cursor.fetchall())
    # 把索引1的数据(date)按照年月日展开
    for i in range(0, len(allData)):
        data = list(allData[i])
        d = data[0]
        data = [d.year, d.month, d.day] + data[1:]
        allData[i] = data
    cursor.close()
    con.close()
    return allData[:-1], getZSByCode(id)[-length:-1]

def initDatasets(allData, dpAllData, lastDay):
    XArr = []
    YArr = []
    lastData = allData[-1]
    n = len(lastData)
    for i in range(len(allData) - lastDay + 1):
        # 将前lastDay的数据拼接起来，作为一条数据模型
        data = allData[i:i+lastDay]
        dpData = dpAllData[i:i+lastDay]
        xData = [n for x in data for n in x] + [n for x in dpData for n in x]
        # 将第3~8位置的数值进行处理
        for j in range(lastDay):
            # v3 = xData[n * j + 3]
            # v4 = xData[n * j + 4]
            # v5 = xData[n * j + 5]
            # v6 = xData[n * j + 6]
            # v11 = xData[n * j + 11]
            # xData[n * j + 3] = v3 - v4 + v11
            # xData[n * j + 4] = v11
            # xData[n * j + 5] = v5 - v4 + v11
            # xData[n * j + 6] = v6 - v4 + v11
            xData[n * j + 7] = xData[n * j + 7] / 1000000000
            xData[n * j + 8] = xData[n * j + 8] / 1000000000000

        XArr.append(xData)
        # 预测第forwardDay天的y
        # 目标数据采样start,end,max,min
        YArr.append([allData[i + lastDay - 1][x] for x in [3, 4, 5, 6]])
    return XArr, YArr

# 按照向量方式学习
def predict2(xp, xa, ya, algorithem, testScore):
    X_train, X_test, y_train, y_test = train_test_split(xa, ya, random_state=42)
    algorithem.fit(X_train, y_train)
    if testScore:
        trainScore = algorithem.score(X_train, y_train)
        testScore = algorithem.score(X_test, y_test)
        print("{} train score:{} test score:{}".format(type(algorithem), trainScore, testScore))
    return algorithem.predict(xp)

# 单个数值分开学习，目前看起来分开学习要强于一起学习
def predict(i, xp, xa, ya, algorithem, testScore):
    X_train, X_test, y_train, y_test = train_test_split(xa, ya[:, i], random_state=42)
    algorithem.fit(X_train, y_train)
    if testScore:
        trainScore = algorithem.score(X_train, y_train)
        testScore = algorithem.score(X_test, y_test)
        print("{} train score:{} test score:{}".format(type(algorithem), trainScore, testScore))
    return algorithem.predict(xp)

# 测试数据使用的5天前的XArr，来预测最近五天的数据，以便和真实数据：最近五天的YArr对比。
# 但考虑到该数据实际上学习过，所以可能出现过拟合的情况。
# 正常情况是使用最近一天的XArr，来预测未来五天的数据
def predictByCode(XArr, YArr, algorithem, forwardDay, testScore):
    # 构造训练数据
    xa = XArr[:len(XArr) - forwardDay]
    ya = np.array(YArr[forwardDay:])
    # print("forwardDay:{} YArr:{}".format(forwardDay, YArr[forwardDay-6]))
    # p = [predict(i, [XArr[-1]], xa, ya, algorithem, testScore) for i in range(len(YArr[0]))]
    p = predict2([XArr[-1]], xa, ya, algorithem, testScore)
    p = [round(x, 2) for n in p for x in n]
    print("algorithem:{} pred:{}".format(algorithem, p))
    return p


def main(code):
    code = str(code)
    testScore = True
    con = connectDB()
    readZS(con)
    allData, dpAllData = readDB(con, code)
    lastDay = 30
    forwardDay = 3
    XArr, YArr = initDatasets(allData, dpAllData, lastDay)
    # algorithems = (MLPRegressor(alpha=1, hidden_layer_sizes=[3,], max_iter=1000), MLPRegressor(solver="lbfgs", alpha=1, hidden_layer_sizes=[3,], max_iter=1000))
    algorithems = (LinearRegression(), LinearRegression(normalize=True), Ridge(), Ridge(normalize=True), Lasso())
    numAlgorithem = len(algorithems)
    allP = []
    try:
        for algo in algorithems:
            arr = []
            allP.append(arr)
            for i in range(forwardDay):
                arr.append(predictByCode(XArr, YArr, algo, i + 1, testScore))
            print()
    except Exception as err:
        print(err)
    # 把allP(n组预测)对位相加再除以行数(同列求均值)，且保留两位小数
    allP = np.array(allP)
    aver = allP[0]
    for n in range(1, len(allP)):
        aver = aver + allP[n]
    aver = np.round(aver / numAlgorithem, 2)
    print("AVERAGE:")
    print(aver)

if len(sys.argv) > 1:
    print("start! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))
    main(sys.argv[1])
    print("over! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))

# main('300015')

sys.exit()