import sys
import pymysql
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import GradientBoostingClassifier

algom = (RandomForestClassifier(), DecisionTreeClassifier(), GaussianNB(), BernoulliNB())

class KLinePredict:
    def connectDB(self)->pymysql.connect:
        con = pymysql.connect(host="localhost", port=3306,user="root",password="123456")
        try:
            # print("open db")
            con.select_db("stock")
        except Exception:
            print("can not find db:stock")
            con.close()
            sys.exit()
        return con

    def readDB(self, con:pymysql.connect, code:str):
        cursor = con.cursor()
        length = 0
        try:
            length = cursor.execute('''select start,end,max,min,voc,tor from s_{} order by date desc limit 300;'''.format(code))
            # print("length:{}".format(length))
        except Exception as err:
            print("select err:{}".format(err))
            sys.exit()
        allData = list(cursor.fetchall())
        cursor.close()
        con.close()
        return allData

    def makeDataset(self, allData):
        xTrain = list()
        yTrain = list()
        xTest = list()
        yTest = list()
        lengh = len(allData)
        for i in range(0, lengh):
            data = list(allData[i])
            start = data[0]
            end = data[1]
            max = data[2]
            min = data[3]
            voc = data[4]
            tor = data[5]
            old = end - voc
            startP = (start / old - 1) * 100
            endP = (end / old - 1) * 100
            maxP = (max / old - 1) * 100
            minP = (min / old - 1) * 100
            xTrain.append((startP, endP, maxP, minP, tor))
            y = 0
            if endP < -7.5:
               y = -4
            elif endP < -5:
               y = -3
            elif endP < -2.5:
               y = -2
            elif endP < 0:
               y = -1
            elif endP < 2.5:
               y = 1
            elif endP < 5:
               y = 2
            elif endP < 7.5:
               y = 3
            else:
               y = 4
            yTrain.append(y)
        xTrain.reverse()
        yTrain.reverse()
        xTrain = xTrain[:-1]
        yTrain = yTrain[1:]
        splitIndex = int(lengh * 0.75)
        xTest = xTrain[splitIndex:]
        yTest = yTrain[splitIndex:]
        xTrain = xTrain[:splitIndex]
        yTrain = yTrain[:splitIndex]
        return xTrain, yTrain, xTest, yTest

    def predict(self, xTrain, yTrain, xTest, yTest):
        rf = GradientBoostingClassifier()
        rf.fit(xTrain, yTrain)
        print(rf.score(xTest, yTest))


    def run(self, code:str):
        con = self.connectDB()
        allData = self.readDB(con, code)
        xTrain, yTrain, xTest, yTest = self.makeDataset(allData)
        self.predict(xTrain, yTrain, xTest, yTest)


if __name__ == '__main__':
    predict = KLinePredict()
    predict.run("300015")

sys.exit()