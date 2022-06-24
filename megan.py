import os
import time
import urllib
from datetime import datetime
import threading
import requests
from bs4 import BeautifulSoup


HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
}
URL_BASE = 'https://mikanani.me'
URL_SEARCH_BASE = 'https://mikanani.me/Home/Search?searchstr='


def doinput():
    inputs = input("Enter your input: ")

    strs = str(inputs)

    return strs


def getcount(list):
    index = 0
    for x in list:
        index += 1
    return index


def selectView(list):
    no = 0
    name = '我全都要'
    print('['+str(no)+'] '+name)
    for x in list:
        no += 1
        name = x[0]
        print('['+str(no)+'] '+name)
    print('[-1] 取消搜索')


def linkurlandname(urls, names):
    ret = []
    temUrl = []
    temName = []

    lengths = 0

    for x in urls:
        lengths += 1
        temUrl.append(URL_BASE+str(x.get('href')))

    for y in names:
        temName.append(str(y.text))

    for z in range(0, lengths):
        ret.append([temName[z], temUrl[z]])

    return ret


def query(url, hearder):

    try:

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#contrainer > div.fire.l > div.pics > ul > li > a'

        resurls = reslxml.select(selecter)

        if(resurls.count == 0):
            return False, []

        urlSelect = '#sk-container > div.central-container > ul > li > a'

        nameSelect = '#sk-container > div.central-container > ul > li > a > div > div > div'

        urlResurls = reslxml.select(urlSelect)

        nameResurls = reslxml.select(nameSelect)

        animes = linkurlandname(urlResurls, nameResurls)

        return True, animes

    except:
        print(1)

        return False, []


def queryvideos(url, hearder):

    try:
        ret = []

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#sk-container > div.central-container > table'

        resurls = reslxml.select(selecter)

        for x in resurls:
            print(x)

        return True, ret

    except:
        print(1)

        return False, []


def search(name):
    url = URL_SEARCH_BASE+name

    checked, animes = query(url, HEADER)

    animeCount = getcount(animes)

    return animeCount, animes


def DoSingleAnimeSave(animepara):
    print('选择：'+animepara[0])

    # 进入动漫页
    checked, videospage = queryvideos(animepara[1], HEADER)

    if(not checked):
        return False
    videosurls = []
    # URL 组装

    # 保存


def main():
    while(1):
        animeName = doinput()
        if(animeName == ''):
            continue
        print('确认到输入的动漫名为：'+animeName)

        counts, animes = search(animeName)

        if(counts == 0):
            print('查询的动漫不存在')
            continue
        elif(counts > 1):
            print('查询到多部请输入序号单个选择或者输入0选择全部：')
            selectView(animes)
            selected = input("Enter your input:")
        elif(counts == 1):
            selected = 1

        if(selected == '-1'):
            print('取消搜索')
            continue
        if(selected != '0'):
            selectanime = int(selected)-1
            animepara = animes[selectanime]
            # 单个动漫保存
            DoSingleAnimeSave(animepara)

            continue
        # 全部保存
        for x in animes:
            DoSingleAnimeSave(x)


main()
