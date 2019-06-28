import BaiduTranslate

if __name__ == "__main__":
    d = BaiduTranslate.Dict()
    json = d.dictionary('今日涨停的股票')
    print(json['trans_result']['data'][0]['dst'])