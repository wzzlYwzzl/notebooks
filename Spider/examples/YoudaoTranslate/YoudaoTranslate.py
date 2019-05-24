import urllib.request
import urllib.parse
import json

content = input('请输入要翻译的句子: ')
youdao_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
baidu_url = 'https://fanyi.baidu.com/transapi'

data = {}
data2 = {}

data['i']= content
data['from'] = 'AUTO'
data['to'] = 'AUTO'
data['smartresult'] = 'dict'
data['client'] = 'fanyideskweb'
data['salt'] = '1525141473246'
data['sign'] = '47ee728a4465ef98ac06510bf67f3023'
data['doctype'] = 'json'
data['version'] = '2.1'
data['keyfrom'] = 'fanyi.web'
data['action'] = 'FY_BY_CLICKBUTTION'
data['typoResult'] = 'false'
data = urllib.parse.urlencode(data).encode('utf-8')

data2['from'] = 'zh'
data2['to'] = 'en'
data2['query'] = content
data2['transtype'] = 'translang'
data2['simple_means_flag'] = '3'
data2['sign'] = '94582.365127'
data2['token'] = 'ec980ef090b173ebdff2eea5ffd9a778'
data2 = urllib.parse.urlencode(data2).encode('utf-8')

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}

youdao_response = urllib.request.urlopen(youdao_url, data)
#baidu_re = urllib.request.Request(baidu_url, data2, headers)
#baidu_response = urllib.request.urlopen(baidu_re)

youdao_html = youdao_response.read().decode('utf-8')
#baidu_html = baidu_response.read().decode('utf-8')

target = json.loads(youdao_html)
#target2 = json.loads(baidu_html)

print('【有道】翻译为: %s'%(target['translateResult'][0][0]['tgt']))
#print('【百度】翻译为: %s'%(target2['trans'][0]['dst']))