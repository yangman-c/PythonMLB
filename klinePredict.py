import sys
import pymysql

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

def readDB(con:pymysql.connect, code:str):
    cursor = con.cursor()
    length = 0
    try:
        length = cursor.execute('''select *from s_{} order by date desc limit 40;'''.format(id))
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

def main(code:int):
    pass

main()

sys.exit()