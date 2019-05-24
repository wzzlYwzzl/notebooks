import urllib.request
import urllib.parse
import json
#txt = input('输入要翻译的内容:')
txt = "今日涨停的股票"

url = 'http://fanyi.so.com/index/search'

data = {
    'query': txt,
    'eng': '0'
}

data = urllib.parse.urlencode(data).encode('utf - 8')
wy = urllib.request.urlopen(url, data)
html = wy.read().decode('utf - 8')
ta = json.loads(html)
print(ta['data']['fanyi'])
