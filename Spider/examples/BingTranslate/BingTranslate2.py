#导入requests模块
import requests
#翻译的内容
#words = input('请输入你要翻译的内容:')
words = "今日涨停的股票"
#翻译的内容,及格式打包成一个字典
data = {
    'text' : words,
    'from' : 'zh-CHS',
    'to' : 'en'
}
#必应翻译翻译时的网址
url = 'https://cn.bing.com/ttranslate?&category=&IG=0DB37A4E4FCB479C990C0EEE9419B058'
#将网址和请求包传入requests模块,以post请求的方式发送出去
result = requests.post(url, data)
#以文本的形式打印结果
print(result.text)
#以json的形式打印结果,并利用索引去除不需要的内容
print(result.json())