import time
from urllib.request import Request, urlopen

def getKLineDayUrl_SZ(tp, id, t)->str:
    return "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124009517967901227564_1597003341751&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid={}.{}&beg=0&end=20500000&_={}".format(tp, id, t)

def getData(code, tp)->str:
    t = int(time.time() * 1000)
    codeHead = code[:3]
    url = getKLineDayUrl_SZ(tp, code, tp)
    req = Request(url)
    respones = None
    try:
        respones = urlopen(url)
    except Exception as err:
        print("err:{}".format(err))
        return "", err
    data = respones.read()
    # print(data)
    return str(data), None

print(getData("603666", 1))