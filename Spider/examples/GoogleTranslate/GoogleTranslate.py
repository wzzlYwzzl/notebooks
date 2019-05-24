"""
测试访问Google翻译
"""

import requests
import json
from googletrans import Translator
import time

def get_proxy_endpoint():
    """获取用于爬取数据的代理IP，调用一次获取一个IP
    """
    url = "http://dwdata.wind.com.cn:7017/GetProxy/GetProxy.do?policyId=TEC_CLOUD"
    resp = requests.get(url, timeout=30)
    if resp.status_code == requests.codes.ok:
        data = json.loads(resp.text)
        ip = data.get("result")[0].get("ip")
        port = data.get("result")[0].get("port")

        return (ip,port)
    return None


service_urls = ['translate.google.cn']
ip_port = ("114.55.30.226", 3129)
proxy = {'http':str(ip_port[0]) + ':' + str(ip_port[1])}
test_file = "/Users/caoxiaojie/Downloads/novel.txt"

f = open(test_file,encoding='utf-8')
lines = f.readlines()
for line in lines:
    if len(line) <= 1:
        continue
    try:
        #ip_port = get_proxy_endpoint()
        translator = Translator(service_urls=service_urls,proxies=proxy,timeout=20)
        #text = '今日涨停的股票'
        res = translator.translate(line, dest='en', src='zh-cn')
        print(res)
        time.sleep(0.1)
    except Exception as e:
        print(e)

"""
ip_pool = {}

for i in range(100000):
    ip,port = get_proxy_endpoint()
    if ip in ip_pool:
        #print('ip:{} 已经存在'.format(ip))
        pass
    else:
        ip_pool[ip] = port

    if i % 100 == 0:
        print('i:{},ip数量：{}'.format(i, len(ip_pool)))
    time.sleep(0.001)

"""