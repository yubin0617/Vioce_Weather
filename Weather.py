import json
from dict import *
import requests

def Weather(city):
    # print(city)
    if(city[-2]=='市'):
        city = city[0:-2]
    if(city[-1]=='。'):
        city=city[0:-1]
    id = compare(city)
    #print(id)
    url='https://api.help.bj.cn/apis/weather/?id='+id
    header = {
        'Host': 'api.help.bj.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'

    }
    res=requests.get(url,headers=header)
    #print(res.text)
    res.encoding='utf-8'
    tmpjson = json.loads(res.text)
    #print(tmpjson)
    tempjson.jsonweather=tmpjson
    print("jsonweather:"+str(tempjson.jsonweather))
    if(tmpjson['status']=="0"):
        temp=list(tmpjson['today'])
        temp[4]='年'
        temp[7]='月'
        tmpjson['today']=''.join(temp)
        weatherStr=(tmpjson['city']+'\n'+tmpjson['today']+'\n'+tmpjson['weather']+'\n'+tmpjson['wd']+
                    tmpjson['wdforce']+'\n'+tmpjson['temp']+'摄氏度'+'\n'+'空气质量指数:'+tmpjson['pm25'])
        print(weatherStr)
        # seter=weatherStr.split("\n")
        # print(seter)
        return weatherStr
    else:
        print('找不到该城市：'+city)
        return ('找不到该城市：'+city)

class tempjson():
    jsonweather = None

tempjson = tempjson()


if __name__ == '__main__':
    Weather('郑州市。')