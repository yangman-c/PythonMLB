import sys
import common.globalConfig as globalConfig
import eastmoney.commonInterface as emInterface
import openpyxl
import random

wb = openpyxl.Workbook()
allIndustrySheet = wb.worksheets[0]
allIndustrySheet.title = "全行业"
allIndustrySheet.append(("行业名称", "总市值", "平均市值", "个股数量", "净资产", "净利润", "市盈率(动)", "市净率", "毛利率", "净利率", "ROE"))


def getInfo(code):
    print(f"handle code:{code}")
    response, err = emInterface.getInfo(code)
    if err != None:
        print(f"getInfo err:{err}")
        print(err.args)
        return True
    try:
        datas = response['data']['diff']
    except Exception as err:
        return
    stockData = datas[0]
    industryData = datas[1]
    # print(stockData)
    # print(industryData)
    行业name = industryData['f14']
    if 行业name not in wb:
        sheet = wb.create_sheet(title=行业name)
        sheet.append(("名称", "总市值", "净资产", "净利润", "市盈率(动)", "市净率", "毛利率", "净利率", "ROE", "总市值排名", "净利润排名", "净资产排名", "市盈率(动)排名", "市净率排名", "毛利率排名", "净利率排名", "ROE排名", "平均行业排名"))
        sheet.append((industryData['f14'], industryData['f2020'], industryData['f2135'], industryData['f2045'], industryData['f2009'], industryData['f2023'], industryData['f2049'], industryData['f2129'], industryData['f2037']))
        allIndustrySheet.append((industryData['f14'], industryData['f20'], industryData['f2020'], industryData['f134'], industryData['f2135'], industryData['f2045'], industryData['f2009'], industryData['f2023'], industryData['f2049'], industryData['f2129'], industryData['f2037']))

    numStocks = industryData['f134']
    rank1 = stockData['f1020']
    rank2 = stockData['f1045']
    rank3 = stockData['f1135']
    rank4 = stockData['f1009']
    rank5 = stockData['f1023']
    rank6 = stockData['f1049']
    rank7 = stockData['f1129']
    rank8 = stockData['f1037']
    wb[行业name].append((stockData['f14'], stockData['f20'], stockData['f45'], stockData['f135'], stockData['f9'], stockData['f23'], stockData['f49'], stockData['f129'], stockData['f37'], f"{rank1}|{numStocks}", f"{rank2}|{numStocks}", f"{rank3}|{numStocks}", f"{rank4}|{numStocks}", f"{rank5}|{numStocks}", f"{rank6}|{numStocks}", f"{rank7}|{numStocks}", f"{rank8}|{numStocks}", f"{int((rank1 + rank2 + rank3 + rank4 + rank5 + rank6 + rank7 + rank8) / 8)}|{numStocks}"))

    # return True

print(f"makeQuartile start")
globalConfig.foreachAllCodes(getInfo)
try:
    wb.save("industry.xlsx")
except Exception as err:
    print(err)
    wb.save(f"industry_{random.random()}.xlsx")
print(f"makeQuartile over")
sys.exit()

# f9:市盈率(动)
# f12:code
# f14:name
# f20:总市值
# f23:市净率
# f37:ROE
# f45:净利润
# f49:毛利率
# f129:净利率
# f135:净资产
# f1020:总市值行业排名
# f1045:净利润行业排名
# f1009:市盈率(动)行业排名
# f1023:市净率行业排名
# f1049:毛利率行业排名
# f1129:净利率行业排名
# f1037:ROE行业排名
# f1135:净资产行业排名
# 总结:后两位数是类别，0开头是个股，1开头是个股在行业排名，2开头是行业平均值
# f12:行业code
# f14:行业name
# f20:行业总市值?
# f134:行业个股数量
# f2020:行业平均市值
# f2045:行业净利润
# f2009:行业市盈率(动)
# f2023:行业市净率
# f2049:行业毛利率
# f2129:行业净利率
# f2037:行业ROE
# f2135:行业净资产