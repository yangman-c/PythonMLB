import sys
import time

import pymysql
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import  train_test_split
from sklearn.linear_model import LinearRegression
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

def readDB(id):
    con = connectDB()
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
    return allData

def initDatasets(allData, lastDay):
    XArr = []
    YArr = []
    lastData = allData[-1]
    n = len(lastData)
    for i in range(len(allData) - lastDay + 1):
        # 将前lastDay的数据拼接起来，作为一条数据模型
        data = allData[i:i+lastDay]
        xData = [n for x in data for n in x]
        # 将第3~8位置的数值进行处理
        for j in range(lastDay):
            xData[n * j + 3] = (xData[n * j + 3] / lastData[3] - 1) * 100
            xData[n * j + 4] = (xData[n * j + 4] / lastData[3] - 1) * 100
            xData[n * j + 5] = (xData[n * j + 5] / lastData[3] - 1) * 100
            xData[n * j + 6] = (xData[n * j + 6] / lastData[3] - 1) * 100
            xData[n * j + 7] = xData[n * j + 7] / 1000
            xData[n * j + 8] = xData[n * j + 8] / 1000000

        XArr.append(xData)
        # 预测第forwardDay天的y
        # 目标数据采样start,end,max,min
        YArr.append([allData[i + lastDay - 1][x] for x in [3, 4, 5, 6]])
    return XArr, YArr

def learn1(X,y,testScore)->LinearRegression:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    liner = LinearRegression()
    liner.fit(X_train, y_train)
    if testScore:
        trainScore = liner.score(X_train, y_train)
        testScore = liner.score(X_test, y_test)
        print("LinearRegression train score:{} test score:{}".format(trainScore, testScore))
    return liner

def learn2(X,y,testScore)->RandomForestRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    forest = RandomForestRegressor(n_estimators=20, random_state=2)
    forest.fit(X_train, y_train)
    if testScore:
        trainScore = forest.score(X_train, y_train)
        testScore = forest.score(X_test, y_test)
        print("RandomForestRegressor train score:{} test score:{}".format(trainScore, testScore))
    return forest

def learn3(X,y,testScore)->DecisionTreeRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    tree = DecisionTreeRegressor(max_depth=4, random_state=0)
    tree.fit(X_train, y_train)
    if testScore:
        trainScore = tree.score(X_train, y_train)
        testScore = tree.score(X_test, y_test)
        print("DecisionTreeRegressor train score:{} test score:{}".format(trainScore, testScore))
    return tree

# 按照向量方式学习
def predict2(xp, xa, ya, algorithem, testScore):
    liner = None
    if algorithem == 1:
        liner = learn1(xa, ya, testScore)
    elif algorithem == 2:
        liner = learn2(xa, ya, testScore)
    elif algorithem == 3:
        liner = learn3(xa, ya, testScore)
    return liner.predict(xp)

# 单个数值分开学习，目前看起来分开学习要强于一起学习
def predict(i, xp, xa, ya, algorithem, testScore):
    liner = None
    if algorithem == 1:
        liner = learn1(xa, ya[:, i], testScore)
    elif algorithem == 2:
        liner = learn2(xa, ya[:, i], testScore)
    elif algorithem == 3:
        liner = learn3(xa, ya[:, i], testScore)
    return liner.predict(xp)

# 测试数据使用的5天前的XArr，来预测最近五天的数据，以便和真实数据：最近五天的YArr对比。
# 但考虑到该数据实际上学习过，所以可能出现过拟合的情况。
# 正常情况是使用最近一天的XArr，来预测未来五天的数据
def predictByCode(XArr, YArr, algorithem, forwardDay, testScore):
    # 构造训练数据
    xa = XArr[:len(XArr) - forwardDay]
    ya = np.array(YArr[forwardDay:])
    # print("forwardDay:{} YArr:{}".format(forwardDay, YArr[forwardDay-6]))
    p = [predict(i, [XArr[-1]], xa, ya, algorithem, testScore) for i in range(len(YArr[0]))]
    # p = predict2([XArr[-1]], xa, ya, algorithem, testScore)
    p = [round(x, 2) for n in p for x in n]
    print("algorithem:{} pred:{}".format(algorithem, p))
    return p


def main(code):
    testScore = True
    allData = readDB(code)
    lastDay = 60
    forwardDay = 3
    XArr, YArr = initDatasets(allData, lastDay)
    allP = [[],[],[]]
    try:
        for i in range(forwardDay):
            allP[0].append(predictByCode(XArr, YArr, 1, i + 1, testScore))
        print()
        for i in range(forwardDay):
            allP[1].append(predictByCode(XArr, YArr, 2, i + 1, testScore))
        print()
        for i in range(forwardDay):
            allP[2].append(predictByCode(XArr, YArr, 3, i + 1, testScore))
        print()
    except Exception as err:
        print(err)
    allP = np.array(allP)
    # 把allP(三组预测)对位相加再除以行数(同列求均值)，且保留两位小数
    allP = allP[0] + allP[1] + allP[2]
    allP = np.round(allP / 3, 2)
    print("AVERAGE:")
    print(allP)

if len(sys.argv) > 1:
    print("start! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))
    main(sys.argv[1])
    print("over! {}".format(time.strftime("%Y/%m/%d %H:%M:%S")))

# main(300015)

sys.exit()