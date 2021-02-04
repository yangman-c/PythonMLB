# 东财自选股操作
import json
from urllib.request import urlopen, Request

class EastMoneyController:
    def __init__(self):
        # 从网页上拔下来的，必须带这个头，否则将被403。这里面可能有登录信息
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
            'Referer': 'http://quote.eastmoney.com/',
            'host': 'myfavor.eastmoney.com',
            'Cookie': 'qgqp_b_id=3815b4a4d87774a2e3ccb5c584ae133e; st_si=08039223976786; p_origin=http%3A%2F%2Fpassport2.eastmoney.com; ct=OfKOBzxLyUwUgTZKBn2OVBknkWRf59rzZeYr9QL8AlpZfNf_PS5ytDxJvz8rO2khwpb_SRoOOTJ9ROH2IwYxZry7BnmCwBK506c0cvQEZphxtgIskI_DOAde-LjcQXWHJzP5_I3PKtimRmavqLu7j7t0fx86iRF8i4l19l8ouAw; ut=FobyicMgeV49XUj9B_m01evqF4A4hiLnvP2qQeO0nI1J_30JWSqygD3tQf199fVaYG-89_P5WGwB7mkIAOJLB2bDsuD8ct8eT_rpwoBgSLibtDpdcCp94y3m7_E19li0AqsQltL2KSXihiHsH2phP549BTMX1SJnwD27byPb81UMXZNdw5F5GH8KtvlsI-cr5Ru3U58yZRTmvd90M_2ChailhqusZ9BnPgQe8RRyU8YQEiJROjxWk2SClWdz6PwHxZODXA2eI2ZBQOdpxdpK29vpyOjKZj1v; pi=7723166100673646%3bb7723166100673646%3b%e8%82%a1%e5%8f%8b0761W5651a%3bkulFa6bHv%2bkCAnGRL%2fqaNI0pwXzRUhnqU1k9ADrkL5lJwiEksbVxLoppaa%2bAUt77Xug80ePUj6mRxsob0ZFzEQQpA2o5xOqQGsbl9UXLRALLPROMkdAS81bjHMS2Ev%2f%2fVTsaQgfghhtTPZbYhXuUa1cyXH5InweMGTOgr%2fuCkgOjsDmIn9helIpjFQU02XpTyHbfn6od%3bq7YjmOXArmdSeJmEPpt%2bM5Ia9ko0BJuzHYcmlINFap7OXbVOI4YjimAsVnW9MXIWksnUeG%2fYOxDe%2bz0A4mCTansyfKKhlZkUypWQnnpzRPk04QMz43eJYsL7kFTKa2oxDrQvXOjv%2bDJDUswEfxONife1%2bFej%2bQ%3d%3d; uidal=7723166100673646%e8%82%a1%e5%8f%8b0761W5651a; sid=136059598; vtpst=|; st_pvi=03185002285832; st_sp=2021-02-04%2022%3A32%3A58; st_inirUrl=http%3A%2F%2Fpassport2.eastmoney.com%2F; st_sn=2; st_psi=20210204223332555-113200301712-2853517140; st_asi=20210204223332555-113200301712-2853517140-Web_so_ss-2',
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
    def checkAndCreateNewGroup(self):
        # 最大分组数为8，若当前已经有8组，则删除第二组(第一组是默认自选，留下的是重点关注的股，从第二分组开始，是每日整理出来的优势股)
        if len(self.ginfolist) >= 8:
            deleteGid = self.ginfolist[1]['gid']
            del self.ginfolist[1]
            self.deleteGroup(deleteGid)
        self.createNewGroup(f"autoGroup{self.ginfolist[len(self.ginfolist) - 1]['gid']}")

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
        response, err = self.sendRequest(url, "addNewCode")
        if err != None:
            print(f"err:{err} code:{code}")
            return


# ctl = EastMoneyController()
# ctl.addNewCode("601100")
# print(f"{time.time()*1000:10.0f}")
# sys.exit()