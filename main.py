import requests
import json
import statistics
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from time import sleep


class getRequest:
    def __init__(self, url, asset, fiat, tradeType, rows, pages, bucket, org, token, dbTimeout, dbUrl, payTypes):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "123",
            "content-type": "application/json",
            "Host": "p2p.binance.com",
            "Origin": "https://p2p.binance.com",
            "Pragma": "no-cache",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }
        self.url = url
        self.dbUrl = dbUrl
        self.bucket = bucket
        self.org=org
        self.token=token
        self.dbTimeout=dbTimeout
        self.asset = asset
        self.fiat = fiat
        self.merchantCheck = True
        self.page = pages
        self.payTypes = payTypes
        self.publisherType = None
        self.rows = rows
        self.tradeType = tradeType
        self.data = {
            "asset": self.asset,
            "fiat": self.fiat,
            "merchantCheck": self.merchantCheck,
            "page": self.page,
            "payTypes": payTypes,
            "publisherType": self.publisherType,
            "rows": self.rows,
            "tradeType": self.tradeType
        }

    def getPrice(self):
        r = requests
        try:
            response = r.post(url=self.url, headers=self.headers, json=self.data)
            jresponse = response.json()
        except Exception as e:
            print(e)
            pass
        medianArray = []

        for adv in jresponse['data']:
            try:
                client = InfluxDBClient(url=self.dbUrl, token=self.token, org=self.org, timeout=self.dbTimeout)
                p = Point(self.fiat).tag("Name",
                                         adv['advertiser']['nickName']).field("price", float(adv['adv']['price']))
                write_api = client.write_api(write_options=SYNCHRONOUS)
                write_api.write(bucket=self.bucket, record=p, org=self.org)
                client.close()
                medianArray.append(float(adv['adv']['price']))
            except Exception as e:
                print(e)
                pass

        try:
            medianPrice = statistics.median(medianArray)
            client = InfluxDBClient(url=self.dbUrl, token=self.token, org=self.org, timeout=self.dbTimeout)
            pM = Point(self.fiat).tag("Name", "median price").field("median-price", float(medianPrice))
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, record=pM, org=self.org)
            client.close()
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    with open('config.json') as config_file:
        config = json.load(config_file)
    while True:
        for i in config['bparams']:
            new_request = getRequest(config['url'], asset=i["asset"], fiat=i['fiat'], tradeType=i['tradeType'],
                                     rows=config['rows'], pages=config['pages'], bucket=config['bucket'],
                                     org=config['org'],
                                     dbUrl=config['dbUrl'], dbTimeout=config['dbTimeout'],
                                     token=config['token'], payTypes=i['payTypes'])
            new_request.getPrice()

        sleep(10)
