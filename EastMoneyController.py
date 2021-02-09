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


# ctl = EastMoneyController()
# ctl.addNewCode("601100")
# print(f"{time.time()*1000:10.0f}")
# sys.exit()