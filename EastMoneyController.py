# 东财自选股操作
import json
from urllib.request import urlopen, Request

class EastMoneyController:
    def __init__(self, cookie: str):
        # 从网页上拔下来的，必须带这个头，否则将被403。这里面可能有登录信息
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
            'Referer': 'http://quote.eastmoney.com/',
            'host': 'myfavor.eastmoney.com',
            'Cookie': f"{cookie}",
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        self.getGroupInfo()

    # 由于有登录人肉验证，所以自动登录暂时没有实现
    def loginEastMoney(self):
        pass

    def sendRequest(self, url:str, methodName:str):
        req = Request(url, headers=self.headers, method="GET")
        try:
            response = urlopen(req)
        except Exception as err:
            print(err)
            return None, err
        response = json.loads(response.read().decode('utf-8'))
        print(f"{methodName}, message:{response['message']}")
        if response['message'] != "成功":
            return response, Exception("response['message']")
        return response, None

    def deleteGroup(self, gid:int):
        url = f"http://myfavor.eastmoney.com/v4/webouter/dg?appkey=d41d8cd98f00b204e9800998ecf8427e&cb=&g={gid}&_="
        respones, err = self.sendRequest(url, "deleteGroup")
        if err != None:
            print(f"err:{err} gid:{gid}")
            return

    # 检测分组状况，并创建新组
    def checkAndCreateNewGroup(self, groupName: str):
        # 最大分组数为8，若当前已经有8组，则删除第二组(第一组是默认自选，留下的是重点关注的股，从第二分组开始，是每日整理出来的优势股)
        if len(self.ginfolist) >= 8:
            deleteGid = self.ginfolist[1]['gid']
            del self.ginfolist[1]
            self.deleteGroup(deleteGid)
        self.createNewGroup(groupName)

    # 创建新组
    def createNewGroup(self, groupName:str):
        url = f"http://myfavor.eastmoney.com/v4/webouter/ag?appkey=d41d8cd98f00b204e9800998ecf8427e&cb=&gn={groupName}&_="
        response, err = self.sendRequest(url, "createNewGroup")
        if err != None:
            print(f"err:{err} groupName:{groupName}")
            return
        self.getGroupInfo()

    def getGroupInfo(self):
        url = "http://myfavor.eastmoney.com/v4/webouter/ggdefstkindexinfos?appkey=d41d8cd98f00b204e9800998ecf8427e&cb=&_="
        response, err = self.sendRequest(url, "getGroupInfo")
        if err != None:
            print(err)
            return
        # {'gid': '1', 'gname': '自选股', 'fromclient': 'web', 'ver': 13}
        self.ginfolist = response['data']['ginfolist']
        print(self.ginfolist)
        print(len(self.ginfolist))

    def addNewCode(self, code: str):
        sc = 1
        head = code[0]
        if head == "0" or head == "3":
            sc = 0
        url = f"http://myfavor.eastmoney.com/v4/webouter/as?appkey=d41d8cd98f00b204e9800998ecf8427e&cb=&g={self.ginfolist[-1]['gid']}&sc={sc}%24{code}&_="
        # url = f"http://myfavor.eastmoney.com/v4/webouter/ag?appkey=d41d8cd98f00b204e9800998ecf8427e&cb=jQuery3310367844530115673_1612534618307&gn=ggg&_=1612534618314"
        response, err = self.sendRequest(url, "addNewCode")
        if err != None:
            print(f"err:{err} code:{code}")
            return

def getSecid(code:str):
    head = code[0]
    if head == "0" or head == "3":
        return 0
    else:
        return 1

def sendRequest(url:str):
    req = Request(url, method="GET")
    print(url)
    try:
        response = urlopen(req)
    except Exception as err:
        print(err)
        return None, err
    return response, None
    # response = json.loads(response.read().decode('utf-8'))
    # print(f"{methodName}, message:{response['message']}")
    # if response['message'] != "成功":
    #     return response, Exception("response['message']")
    # return response, None

def getInfo(code):
    url = f"http://push2.eastmoney.com/api/qt/slist/get?spt=1&np=3&fltt=2&invt=2&fields=f9,f12,f13,f14,f20,f23,f37,f45,f49,f134,f135,f129,f1000,f2000,f3000&ut=bd1d9ddb04089700cf9c27f6f7426281&cb=&secid={getSecid(code)}.{code}&_="
    response, err = sendRequest(url)
    if err != None:
        print(f"err:{err} code:{code}")
        return
    print(response.read().decode('utf-8'))

# ctl = EastMoneyController()
# ctl.addNewCode("601100")
# print(f"{time.time()*1000:10.0f}")
# sys.exit()

# if __name__ == '__main__':
#     getInfo("600031")
    # "{"rc":0,"rt":18,"svr":2887254207,"lt":1,"full":1,"data":{"total":2,"diff":[{"f9":24.1,"f12":"600031","f13":1,"f14":"三一重工","f20":400023352428,"f23":7.5,"f37":24.06,"f45":12450341000.0,"f49":30.3009,"f129":17.4689,"f134":"-","f135":54901439000.0,"f1020":1,"f1113":47,"f1045":1,"f1009":60,"f1023":217,"f1049":75,"f1129":33,"f1037":7,"f1135":2,"f1115":68,"f1058":1,"f1132":2,"f1130":174,"f1131":110,"f1137":86,"f1133":86,"f1138":86,"f2020":0.0,"f2113":0.0,"f2045":0.0,"f2009":0.0,"f2023":0.0,"f2049":0.0,"f2129":0.0,"f2037":0.0,"f2135":0.0,"f2115":0.0,"f2058":0.0,"f2132":0.0,"f2130":0.0,"f2131":0.0,"f2137":0.0,"f2133":0.0,"f2138":0.0,"f3020":1,"f3113":1,"f3045":1,"f3009":2,"f3023":4,"f3049":2,"f3129":1,"f3037":1,"f3135":1,"f3115":2,"f3058":1,"f3132":1,"f3130":3,"f3131":2,"f3137":2,"f3133":2,"f3138":2},{"f9":29.68,"f12":"BK0545","f13":90,"f14":"机械行业","f20":2526281376000,"f23":"-","f37":"-","f45":"-","f49":"-","f129":"-","f134":239,"f135":"-","f1020":0,"f1113":0,"f1045":0,"f1009":0,"f1023":0,"f1049":0,"f1129":0,"f1037":0,"f1135":0,"f1115":0,"f1058":0,"f1132":0,"f1130":0,"f1131":0,"f1137":0,"f1133":0,"f1138":0,"f2020":10503206807.06,"f2113":4.74,"f2045":237746193.5,"f2009":74.4,"f2023":3.63,"f2049":25.39,"f2129":4.4,"f2037":4.56,"f2135":3507441459.54,"f2115":5.93,"f2058":3246439658.84,"f2132":4497848852.06,"f2130":4.79,"f2131":49.11,"f2137":0.0,"f2133":0.0,"f2138":0.0,"f3020":5,"f3113":5,"f3045":5,"f3009":5,"f3023":5,"f3049":5,"f3129":5,"f3037":5,"f3135":5,"f3115":5,"f3058":5,"f3132":5,"f3130":5,"f3131":5,"f3137":5,"f3133":5,"f3138":5}]}}
#"