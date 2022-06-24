import os
import time
import urllib
from datetime import datetime
import threading
from lxml import etree

import requests
from bs4 import BeautifulSoup

# 1 33 40

inputs = input("Enter your input: ")

strs = str(inputs)

print('确认到输入的用户ID为：'+strs)

USERID = strs

userdata = {
    # 用户名
    'username': '',

    # 总发帖数
    'allitems': 0,
    # 总浏览数
    'allviews': 0,
    # 总回复数
    'allrecall': 0,
    # 总点赞数
    'allyes': 0,
    # 总收藏数
    'allsave': 0,

    # 平均浏览数
    'avaViews': 0,
    # 平均回复数
    'avarecall': 0,
    # 平均点赞数
    'avayes': 0,
    # 平均收藏数
    'avasave': 0,

    # 最高浏览数
    'maxViews': 0,
    # 最高回复数
    'maxrecall': 0,
    # 最高点赞数
    'maxyes': 0,



}


header = {
    'cookie': 'bbs_token=P62jCVsWr9504BF_2F7Iq0cjSsOikTV423qIdkfuTJlXEg_2Fp0eE4MD3MHQ6nw_2Fzk_2FBTyw8_2FxFV5iulMqNjAcyOzA_3D_3D; bbs_sid=458013c9035834363c49487a843e3def; UM_distinctid=17c7c5991345db-070396d0205a9e-513c1e45-32a000-17c7c59913583f; atarget=n; CNZZDATA1277689586=267366360-1634168641-|1637406544',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',

}
session = requests.session()
requests.packages.urllib3.disable_warnings()


url = "https://www.scboy.cc/?user-thread-"+USERID+".htm"


res = session.get(url, headers=header, verify=False)

res.encoding = 'utf-8'

reslxml = BeautifulSoup(res.text, 'lxml')

selecterMaxpath = '#user_main > div > div.card-body > nav > ul > li> a'

selecterusername = '#user_aside > div > div.card-body.text-center'

# strMaxpath = (reslxml.select(selecterMaxpath))[0].get('href')

maxpathTemp = reslxml.select(selecterMaxpath).__len__()

maxpath = maxpathTemp-1
if(maxpathTemp == 12):
    maxpath = int(((reslxml.select(selecterMaxpath))[10].get(
        'href').split('-')[3]).split('.')[0])

if(maxpathTemp == 0):
    maxpath = 1


username = str((reslxml.select(selecterusername)[0]).text).replace('\n', '')

username = username.replace('关注', '')
username = username.replace('\t', '')
username = username.replace('\r', '')

userdata['username'] = username

print('查询到用户：'+username)

time.sleep(0.5)


def getdata(index, header, session):

    data = []
    print('')
    print('计算数据中===========================>')
    print('')
    try:

        for x in range(index):

            baseurl = "https://www.scboy.cc/?user-thread-" + \
                USERID+""+'-'+str(x+1)+".htm"
            res = session.get(baseurl, headers=header, verify=False)
            res.encoding = 'utf-8'
            reslxml = BeautifulSoup(res.text, 'lxml')

            selecterLength = "#user_main > div > div.card-body > ul > li"
            Length = reslxml.select(selecterLength).__len__()

            for y in range(Length):
                ret = []
                selecterwatch = '#user_main > div > div.card-body > ul > li:nth-child('+str(
                    2+y)+') > div.media-body > div.d-flex.justify-content-between.small.mt-1 > div.text-muted.small > span:nth-child(2)'
                selecterthink = '#user_main > div > div.card-body > ul > li:nth-child('+str(
                    2+y)+') > div.media-body > div.d-flex.justify-content-between.small.mt-1 > div.text-muted.small > span:nth-child(3)'
                selecteryes = '#user_main > div > div.card-body > ul > li:nth-child('+str(
                    2+y)+') > div.media-body > div.d-flex.justify-content-between.small.mt-1 > div.text-muted.small > span:nth-child(4)'
                selectersave = '#user_main > div > div.card-body > ul > li:nth-child('+str(
                    2+y)+') > div.media-body > div.d-flex.justify-content-between.small.mt-1 > div.text-muted.small > span:nth-child(5)'
                ret.append(int((reslxml.select(selecterwatch)[0]).text))
                ret.append(int((reslxml.select(selecterthink)[0]).text))
                ret.append(int((reslxml.select(selecteryes)[0]).text))
                ret.append(int((reslxml.select(selectersave)[0]).text))

                data.append(ret)
    except:

        return data

    return data


def exec(data):

    allitems = data.__len__()
    userdata['allitems'] = str(allitems)

    # 除数修正
    if(allitems == 0):
        allitems = 1

    allviews = 0
    allrecall = 0
    allyes = 0
    allsave = 0
    avaViews = 0
    avarecall = 0
    avayes = 0
    avasave = 0
    maxViews = 0
    maxrecall = 0
    maxyes = 0

    for x in data:
        allviews += x[0]
        if(x[0] > maxViews):
            maxViews = x[0]
        allrecall += x[1]
        if(x[1] > maxrecall):
            maxrecall = x[1]
        allyes += x[2]
        if(x[2] > maxyes):
            maxyes = x[2]
        allsave += x[3]

    avaViews = format(
        allviews / allitems, '.4f')
    avarecall = format(
        allrecall / allitems, '.4f')
    avayes = format(
        allyes / allitems, '.4f')
    avasave = format(
        allsave / allitems, '.4f')

    # 空帖修正
    if(allviews == 0):
        userdata['allitems'] = '0'

    userdata['allviews'] = str(allviews)
    userdata['allrecall'] = str(allrecall)
    userdata['allyes'] = str(allyes)
    userdata['allsave'] = str(allsave)
    userdata['avaViews'] = str(avaViews)
    userdata['avarecall'] = str(avarecall)
    userdata['avayes'] = str(avayes)
    userdata['avasave'] = str(avasave)
    userdata['maxViews'] = str(maxViews)
    userdata['maxrecall'] = str(maxrecall)
    userdata['maxyes'] = str(maxyes)

    texts = 'SCBOY论坛用户'+userdata['username']+',全部发帖'+userdata['allitems']+'贴,其全部阅读量为:'+userdata['allviews'] + \
        ',共有'+userdata['allrecall']+'层回复楼层,' \
            '有'+userdata['allyes']+'点赞,'+userdata['allsave']+'收藏。'
    texts2 = '其中平均每个帖子收获'+userdata['avaViews']+"阅读,平均每贴收获回复有" + \
        userdata['avarecall']+'层,'+userdata['avayes'] + \
        '点赞,'+userdata['avasave']+'收藏。'

    texts3 = '全部帖子中,最高浏览量为:'+userdata['maxViews']+',最高回复数为:' + \
        userdata['maxrecall']+',最高点赞数为'+userdata['maxyes']+'。'

    print(str(texts))
    print(str(texts2))
    print(str(texts3))
    print('')
    print('===========================>计算完成！')


exec(getdata(int(maxpath), header, session))
