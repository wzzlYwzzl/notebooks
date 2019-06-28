import urllib.request
import urllib.parse
import json

url = 'http://fy.iciba.com/ajax.php?a=fy'
txt = "今日涨停的股票"
data = {
    'f': 'auto',
    't': 'auto',
    'w': txt
}

data = urllib.parse.urlencode(data).encode('utf - 8')
wy = urllib.request.urlopen(url, data)
html = wy.read().decode('utf - 8')
ta = json.loads(html)
print(ta['content']['out'])
