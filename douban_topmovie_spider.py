import requests
from selenium import webdriver
from bs4 import BeautifulSoup

link =""" """
def get_movies():
    headers = {
        'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Host':'movie.douban.com'
        }

    movie_list=[]
    movie_detail_list=[]
    for i in range(0,1):
        link = 'https://movie.douban.com/top250?start='+str(i*25)

        r=requests.get(link,headers=headers,timeout=10)
        print(str(i+1),"响应：",r.status_code)
        soup=BeautifulSoup(r.text,"lxml")
        div_list = soup.find_all('div',class_='hd')
        div_list2= soup.find_all('div',class_='bd')

        #print(div_list)
        for each in div_list:
            movie= each.a.span.text.strip()
            movie_list.append(movie)

        for each in div_list2:
            movie_detail=each.p.text.strip()
            movie_detail_list.append(movie_detail)


    return movie_list,movie_detail_list



movies,details= get_movies()
print(movies)
print(details[1:])