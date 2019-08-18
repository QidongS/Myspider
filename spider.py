from utils import Util
from bs4 import BeautifulSoup
import json
import re
import pymysql


#https://rate.tmall.com/list_detail_rate.htm?itemId=563449442655&spuId=349188091&sellerId=3602204308&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvPQvEvbQvUvCkvvvvvjiPRFdv0jDCR25vtjljPmPWgjrPPFLv0jtUn25p0jtn3QhvChCCvvmtvpvIphvvfvvvphCvpvskvvCvghCvjvUvvhBGphvwv9vvpqYvpvQ2vvC2STyCvv3vpvo1ZhMwaOyCvvXmp99UetIEvpCWBPofv8RKNB9f8zxr%2Bull8C61iNo4ezXvfCuYiLUpwh%2BFp%2B0xhE3zLLEc6aZtn0vHVADlYC978BB1pns9V1O07oDn9Wma%2BoHoEpchgvhCvvXvovvvvvvPvpvhvv2MMsyCvvBvpvvviQhvChCvCCp%3D&needFold=0&_ksTS=1566062859918_906&callback=jsonp907

util = Util()

def getCommentDetail(itemId,sellerId,currentPage):
    '''
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId) +\
          '&spuId=349188091&sellerId=' +str(sellerId)+'&order=3&currentPage='+str(currentPage)+'&append=0callback=jsonp1729'
        '''
    url=' https://rate.tmall.com/list_detail_rate.htm?itemId=563449442655&spuId=349188091&sellerId=3602204308&order=3&currentPage=1&append=0callback=jsonp907'

    html =util.getUrlContent(url)
    #soup = BeautifulSoup(html,'html.parser')

    print(html)
    html = html.replace('jsonp','')
    html = re.sub('\d\d\d.','',html)
    html = html.replace(')',"")
    html = html.replace('false',"false")
    html = html.replace('true',"true")


    productjson= json.loads(html)
    return productjson


getCommentDetail(563449442655,3602204308,1)