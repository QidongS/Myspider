#https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26q%3D%2347.6%E4%B8%87%E4%BA%BA%E5%8F%82%E4%B8%8E%E5%8F%8D%E6%9A%B4%E5%8A%9B%E6%95%91%E9%A6%99%E6%B8%AF%E9%9B%86%E4%BC%9A
import requests
import re
import os
import csv
import json
import time
import random

min_time_id= ''
s= requests.Session()

def get_topic(page=0):
    global min_time_id
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26q%3D%2347.6%E4%B8%87%E4%BA%BA%E5%8F%82%E4%B8%8E%E5%8F%8D%E6%9A%B4%E5%8A%9B%E6%95%91%E9%A6%99%E6%B8%AF%E9%9B%86%E4%BC%9A &page='+str(page)
    if min_time_id:
        url = url+'&since_id='+min_time_id
    header = {
        'user-agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36',
        'Referer' : 'https://m.weibo.cn/search?containerid=231522type%3D1%26q%3D%2347.6%E4%B8%87%E4%BA%BA%E5%8F%82%E4%B8%8E%E5%8F%8D%E6%9A%B4%E5%8A%9B%E6%95%91%E9%A6%99%E6%B8%AF%E9%9B%86%E4%BC%9A%23'

    }

    try:
        r= s.get(url=url,headers=header)
        r.raise_for_status()
    except:
        print("spider died")
    #print(r.text)

    #extract json
    r_json = json.loads(r.text)
    print(r_json)
    cards = r_json['data']['cards']
    '''
    if len(cards) > 1 :
        card_group = cards[2]['card_group']
    else:
        card_group= cards[0]['card_group']
    '''

    #print(cards)



    for i in range(len(cards)):
        if len(cards) > 1 and i<=1:
            continue

        card_group =cards[i]['card_group']  #  possible there's no 'card group'
        for card in card_group:
            column = []
            try:
                mblog = card['mblog']
                user = mblog['user']
                #print("user:",user)
                basic_info = get_user_detail(user['id'])
                #print("basic info--->", basic_info)
                # except:
                #     print("bad user info ")
                #     continue

                column.append(user['id'])
                column.extend(basic_info)

                r_time_id = mblog['id']

                text_only = re.compile(r'<[^>]+>', re.S).sub(' ',mblog['text'])
                clean_text = text_only.replace('#反暴力救香港#',' ')
                clean_text = clean_text.replace('#47.6万人参与反暴力救香港集会#', ' ')
                column.append(clean_text)
                '''
                if min_time_id:
                    print("------------->"+r_time_id)
                    min_time_id = r_time_id if min_time_id> r_time_id else min_time_id
                else:
                    min_time_id = r_time_id
                '''

                #print(clean_text)
                if len(column)<6:
                    print("Incomplete weibo post")
                    continue

                #save_data(column)
                print("---------------------------------------------------------")
                print(column)
                print("---------------------------------------------------------")
                time.sleep(random.randint(3,6))

            except KeyError as e:
                print(e)
                continue

def user_login():

    url = "https://passport.weibo.cn/sso/login"
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36',
        'Referer' : 'https://passport.weibo.cn/signin/login'

    }
    data= {
        'username' : '0015107782191',
        'password' : '',
        'savestate': 1,
        'entry' : 'mweibo',
        'mainpageflag' : 1

    }

    try:
        r=s.post(url,headers=header,data=data)
        r.raise_for_status()
    except:
        print("login failure")
        return 0
    #print(json.loads(r.text))
    return 1


def get_user_detail(id):
    '''

    :param id: post owner's user id
    :return: ['username','gender','area','birthday']
    '''
    url = 'https://weibo.cn/'+str(id)+'/info'
    #print(url)
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'

    }

    try:
        r = s.get(url=url, headers=header)
        #print(r.text)
        r.raise_for_status()
    except:
        print("user info failure")
        return
    #use re lib to extract data we need
    info_html= re.findall('<div class="tip">基本信息</div><div class="c">(.*?)</div>', r.text)
    #print(info_html)
    info = get_info_list(info_html)
    return info

def get_info_list(info_html) -> list:
    '''

    :param info_html:
    :return: [username,gender, area, birthday]
    '''
    info_list = []
    basic_info_kvs = info_html[0].split('<br/>')
    #print(basic_info_kvs)
    for basic_info_kv in basic_info_kvs:
        if basic_info_kv.startswith('昵称'):
            info_list.append(basic_info_kv.split(':')[1])
        elif basic_info_kv.startswith('性别'):
            info_list.append(basic_info_kv.split(':')[1])
        elif basic_info_kv.startswith('地区'):
            area=basic_info_kv.split(':')[1]
            if '其他' in area or '海外' in area:
                info_list.append('')
                continue
            if ' ' in area:
                area = area.split(' ')[0]
            info_list.append(area)
        elif basic_info_kv.startswith('生日'):
            birthday = basic_info_kv.split(':')[1]
            #print(birthday)
            if birthday.startswith('19') or birthday.startswith('20'):
                info_list.append(birthday[:])
            else:
                info_list.append('')
        else:
            pass
    #in case no birthday
    print(info_list)
    if len(info_list)<4:
        info_list.append('')
    return info_list

def auto_run():
    #must login first
    if not user_login():
        return
    for i in range(3):
        get_topic(i)

#print(user_login())

if __name__ == '__main__':
    auto_run()
#user_login()
#get_user_detail(2803301701)