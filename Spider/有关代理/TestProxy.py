'''
用于测试代理IP是否有效
'''

import requests

#高匿代理
proxy_high = 'http://119.196.187.52:80'
proxy_high = 'http://101.132.133.234'

#普匿代理
proxy_ord = 'http://115.159.121.38:80'

#透明代理
proxy_transparent = 'http://114.55.92.9:9999'
#proxy_transparent = 'http://222.175.171.6:8080'
proxy_transparent = 'http://119.57.105.25:53281'

proxy = {'https':proxy_transparent}

url = 'https://httpbin.org/get'
url2 = 'https://ifconfig.me'
url3 = 'http://icanhazip.com'

if __name__ == '__main__':
    resp = requests.get(url, proxies=proxy)
    print(resp.text)
