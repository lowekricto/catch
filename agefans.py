import os
import time
import urllib
import math
from datetime import datetime
import threading
from lxml import etree

import requests
from bs4 import BeautifulSoup


def getCount(url, header):
    try:

        res = requests.get(url, headers=header)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#result_count'

        resurls = reslxml.select(selecter)

        ret = (resurls[0].text).replace('纪录', '')

        return ret

    except:
        return []


def urlmakebase(urls):
    baseurl = 'https://www.agefans.vip'
    ret = []
    for x in urls:
        url = baseurl+x.get('href')

        ret.append(url)
    return ret


def find(url, header):

    try:

        res = requests.get(url, headers=header)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#container > div:nth-child(4) > div > div > div > div:nth-child(1) > a'

        resurls = reslxml.select(selecter)

        ret = urlmakebase(resurls)

        return ret

    except:
        return []


def query(url, header):

    res = requests.get(url, headers=header)

    res.encoding = 'utf-8'

    reslxml = BeautifulSoup(res.text, 'lxml')

    selecter = '#container > div.div_right > div:nth-child(1) > div'

    resurls = reslxml.select(selecter)

    name = str(resurls[0].text).replace('\n', '')


    return name, '1'


def main():

    url = 'https://www.agefans.vip/catalog/all-2021-all-all-all-time-1-%E6%97%A5%E6%9C%AC-all-all'
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    }
    count = int(getCount(url, header))
    page = math.ceil(count/24)

    for x in range(1, page+1):
        url = 'https://www.agefans.vip/catalog/all-2021-all-all-all-time-' + str(x) + \
            '-%E6%97%A5%E6%9C%AC-all-all'

        aUrls = find(url, header)

        for x in aUrls:

            name, aurl = query(x, header)
            break
        break


main()
