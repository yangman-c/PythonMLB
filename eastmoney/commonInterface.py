import json
from urllib.request import urlopen, Request


def getSecid(code: str):
    head = code[0]
    if head == "0" or head == "3":
        return 0
    else:
        return 1


def sendRequest(url: str):
    req = Request(url, method="GET")
    try:
        response = urlopen(req)
    except Exception as err:
        print(err)
        return None, err
    response = json.loads(response.read().decode('utf-8'))
    return response, None


def getInfo(code):
    # 原始参数
    # url = f"http://push2.eastmoney.com/api/qt/slist/get?spt=1&np=3&fltt=2&invt=2&fields=f9,f12,f13,f14,f20,f23,f37,f45,f49,f134,f135,f129,f1000,f2000,f3000&ut=bd1d9ddb04089700cf9c27f6f7426281&cb=&secid={getSecid(code)}.{code}&_="
    # 简化参数
    url = f"http://push2.eastmoney.com/api/qt/slist/get?spt=1&np=3&fltt=2&invt=2&fields=f9,f12,f14,f20,f23,f37,f45,f49,f129,f134,f135,f1000,f2000&secid={getSecid(code)}.{code}"
    response, err = sendRequest(url)
    if err != None:
        print(f"err:{err} code:{code}")
        return None, err
    return response, None