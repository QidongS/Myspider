import requests
import time
import random
import socket
import http.client
import pymysql
import csv

class Util(object):
    def getUrlContent(self,url,data=None):
        header = {
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "cache-control" : "max-age=0"
        }

        timeout = random.choice(range(80,100))

        while True:
            try:
                r=requests.get(url,headers=header,timeout=timeout)
                break;
            except socket.timeout as e:
                print('3:',e)
                time.sleep(random.choice(range(8,15)))
            except socket.error as e:
                print('4:', e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e :
                print("5:",e)
                time.sleep(random.choice(range(20,60)))
            except http.client.IncompleteRead as e :
                print("6:",e)
                time.sleep(random.choice(range(5,15)))

        print('request success')
        return r.text

#def writeData(self,data,url):
