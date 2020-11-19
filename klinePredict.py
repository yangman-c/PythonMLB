import sys
import pymysql

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
            length = cursor.execute('''select start,end,max,min,voc,tor from s_{} order by date desc limit 120;'''.format(code))
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
            startP = start / old - 1
            endP = end / old - 1
            maxP = max / old - 1
            minP = min / old - 1
            xTrain.append((startP, endP, maxP, minP, tor))
            yTrain.append(endP)
        xTrain = xTrain[:-1]
        yTrain = yTrain[1:]
        splitIndex = int(lengh * 0.75)
        xTest = xTrain[splitIndex:]
        yTrain = yTrain[splitIndex:]
        xTrain = xTrain[:splitIndex]
        yTrain = yTrain[:splitIndex]
        return xTrain, yTrain, xTest, yTest

    def run(self, code:str):
        con = self.connectDB()
        allData = self.readDB(con, code)
        self.makeDataset(allData)


if __name__ == '__main__':
    predict = KLinePredict()
    predict.run("300015")

sys.exit()