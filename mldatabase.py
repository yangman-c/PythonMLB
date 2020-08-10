import sys
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
    for i in range(len(allData) - lastDay + 1):
        # 将前lastDay的数据拼接起来，作为一条数据模型
        data = allData[i:i+lastDay]
        XArr.append([n for x in data for n in x])
        # 预测第forwardDay天的y
        # 目标数据采样start,end,max,min
        YArr.append([allData[i + lastDay - 1][x] for x in [3, 4, 5, 6]])
    return XArr, YArr

# 构造训练数据
def makeTrainingData(allData, lastDay, forwardDay):
    XArr = []
    YArr = []
    for i in range(len(allData) - lastDay - forwardDay):
        # 将前lastDay的数据拼接起来，作为一条数据模型
        data = allData[i:i+lastDay]
        XArr.append([n for x in data for n in x])
        # 预测第forwardDay天的y
        # 目标数据采样start,end,max,min
        YArr.append([allData[i + lastDay + forwardDay][x] for x in [3, 4, 5, 6]])
    # print(len(XArr), len(YArr), len(XArr[0]),len(YArr[0]))
    return XArr, np.array(YArr)

def learn1(X,y,testScore)->LinearRegression:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    liner = LinearRegression()
    liner.fit(X_train, y_train)
    if testScore:
        trainScore = liner.score(X_train, y_train)
        testScore = liner.score(X_test, y_test)
        print("LinearRegression train score:{} test score:{}".format(trainScore, testScore))
    return liner

def learn2(X,y,testScore)->RandomForestRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    forest = RandomForestRegressor(n_estimators=5, random_state=2)
    forest.fit(X_train, y_train)
    if testScore:
        trainScore = forest.score(X_train, y_train)
        testScore = forest.score(X_test, y_test)
        print("RandomForestRegressor train score:{} test score:{}".format(trainScore, testScore))
    return forest

def learn3(X,y,testScore)->DecisionTreeRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
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

def predictByCode(XArr, YArr, algorithem, forwardDay, testScore):
    # XArr, YArr = makeTrainingData(XArr, YArr, lastDay, forwardDay)
    # 构造训练数据
    xa = XArr[:len(XArr) - forwardDay]
    ya = np.array(YArr[forwardDay:])
    print("forwardDay:{} YArr:{}".format(forwardDay, YArr[forwardDay-6]))
    # p = [predict(i, [XArr[-6]], xa, ya, algorithem, testScore) for i in range(len(YArr[0]))]
    p = predict2([XArr[-6]], xa, ya, algorithem, testScore)
    p = [round(x, 2) for n in p for x in n]
    print("algorithem:{} pred:{}".format(algorithem, p))


def main(code):
    testScore = False
    allData = readDB(code)
    XArr, YArr = initDatasets(allData, 30)
    try:
        for i in range(5):
            predictByCode(XArr, YArr, 1, i + 1, testScore)
        print()
        for i in range(5):
            predictByCode(XArr, YArr, 2, i + 1, testScore)
        print()
        for i in range(5):
            predictByCode(XArr, YArr, 3, i + 1, testScore)
        print()
    except Exception as err:
        print(err)

if len(sys.argv) > 1:
    main(sys.argv[1])

# main("002300")

sys.exit()