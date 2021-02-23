from urllib.request import urlopen, Request
from urllib.parse import urlencode
import sys
import gzip
import json
import os
import hashlib

preUploadUrl = "https://pan.baidu.com/api/precreate?channel=chunlei&web=1&app_id=250528&bdstoken=32d10c1c21387b0c533701d09b627db5&logid=MERCMTkwNTVFOEEwQUQ1ODZGMEJBRUI2QzU1MzBENDQ6Rkc9MQ==&clienttype=0"


cookie = "BAIDUID=0DB19055E8A0AD586F0BAEB6C5530D44:FG=1; BIDUPSID=0DB19055E8A0AD586F0BAEB6C5530D44; PSTM=1563520770; BDUSS=k4WE5vYmpJeVdaZ29QZWlJS09kamtOWmk5Q0hwVVRabX5qRXpqQmhnZ2N4MlZmRVFBQUFBJCQAAAAAAAAAAAEAAAD6iPoxaGVwZW5ncWlfb25seQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABw6Pl8cOj5fej; MCITY=-131%3A; __yjs_duid=1_d38cf9f816ad4afc252876423f8d0b621611586415257; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1613992869; BDSFRCVID=4UFOJeC62lecVvOe-kRBb4VW3j352P5TH6ao_lqQNsjB9Y8NvfPHEG0PVf8g0KubzrQPogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tJ-toKDhtI83fP36qROq-tuBMfofKRDXKK_sbCj2BhcqEIL4K4OZMb07btKD5xJaJNcUob56WbQESMbSj4Qo3jkujbnEXlo3yjnqax3o3l5nhMJb257JDMP0-l3OKMJy523ion6vQpn-KqQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xb6_0DToyjHtfJ6-s-KOhLnbObbu_JR71q4bohDCShG4jBn39WDTmWlnnbJjdDb7N2J6fjPj33RteKxnitIv9-pnsanrGjqRgjluB3nJ0ebjZKxtq3mkjbPbDfn02OP5P5q3OMt4syP4jKMRnWnciKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCF5hD8GjTtajTPyhUjJKPRfatoEWb48Kb7VKROkeUI-LU4pbtbLBUJqKmJQWb5XMfTDHCbK3TbqyUnQbPnnBP7QaH602n-KyCTRqIK93x6qLTKkQN3T-PKO5bRiLRoaLnvEDn3oyT3JXp0nj4Rly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfJAD_KD2JCt3H48k-4QEbbQH-UnLq5OwX2OZ04n-ah05SlRaDP_VM-07-GOpL5Jg-a5bhC5m3UTdfh76Wh35K5tTQP6rLtb9tTn4KKJxbU7F8lQh0Kcay4DVhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC_Gj5KaDTvWeUcEhR-XfR6fLb48Kb7VbIbaQxnkbfJBDxv-5h5qBKILBMoPKDb4SIOFDT_K05L7yajK2hRQ-G6wQbcPfxIW84QI0M7pQT8r3xDOK5OibCrEQfjxab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDDoK_bfxK; H_PS_PSSID=33425_33438_33344_33600_33585_33320; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=2; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; BA_HECTOR=0l8401ah2h2ha12gfk1g374l00r; csrfToken=8C5TOVShrGiSgrJ1-LfSYte0; STOKEN=1b5fda01fabe6dc0660ca9bfddab75e6bdba8275268588d2e593848477080e18; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1613992611; PANPSC=5814337157025898443%3ACU2JWesajwCzOuF7eGt6IsJKt428qvGuYRSWom%2BuWt9EH7TSGHkjagjn4HR56dePXrc11mEi6oCgySxxLHkB9INJiGXSx6XUqIvcQmWBLvENZLEPdqOdHV9l5VLCkYtGsG7YZLnfZ%2BWv%2BjYtLTMR3kI0NZhR03fFueSOQr2pfpJ9bfFV5UX2VQ%3D%3D"

preHeads2= {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Content-Length': '124',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': f"{cookie}",
    'Host': 'pan.baidu.com',
    'Origin': 'https://pan.baidu.com',
    'Referer': 'https://pan.baidu.com/disk/home?_at_=1613992608820',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'X-Requested-With': 'XMLHttpRequest',
}

def preLoad(url:str, headers:str, data:str):
    data = urlencode(data)
    data = bytes(data, "utf-8")
    pRequest = Request(url= url, method="POST", headers=headers, data=data)
    try:
        response = urlopen(pRequest)
    except Exception as err:
        print(err)
        return None, err
    response = response.read()
    response = gzip.decompress(response)
    response = json.loads(response)
    print(response)
    return response, None


uploadUrl = "https://pan.baidu.com/api/create?isdir=0&rtype=1&channel=chunlei&web=1&app_id=250528&bdstoken=32d10c1c21387b0c533701d09b627db5&logid=MERCMTkwNTVFOEEwQUQ1ODZGMEJBRUI2QzU1MzBENDQ6Rkc9MQ==&clienttype=0"

preHeads1= {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': f"{cookie}",
    'Host': 'pan.baidu.com',
    'Origin': 'https://pan.baidu.com',
    'Referer': 'https://pan.baidu.com/disk/home?_at_=1613992608820',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'X-Requested-With': 'XMLHttpRequest',
}

def makeRequestData(path:str, size:str, md5:str):
    return {
        "path":f"{path}",
        "size":size,
        "target_path":"/",
        "block_list":f"[\"{md5}\"]",
        "local_mtime":"1514974495"
    }

def makePreLoadData(path:str, md5:str):
    return {
            "path": f"{path}",
            "autoinit": "1",
            "target_path": "/",
            "block_list": f"[\"{md5}\"]",
            "local_mtime": "1514974495"
    }

def getFileMd5(filePath:str):
    try:
        f = open(filePath, 'rb')
    except Exception as err:
        if err != None:
            return None, err
    return hashlib.md5(f.read()).hexdigest()

# path = "D:/bbt.txt"
path = "D:/babyabc.txt"
md5 = getFileMd5(path)
size = os.path.getsize(path)

filename = path[path.rindex("/"):]

preLoadData = makePreLoadData(filename, md5)
preLoad(preUploadUrl, preHeads1, preLoadData)

uploadData = makeRequestData(filename, size, md5)
preLoad(uploadUrl, preHeads1, uploadData)
sys.exit()