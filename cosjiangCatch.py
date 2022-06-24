import os
import time
import urllib
from datetime import datetime
import threading

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from requests.models import CaseInsensitiveDict


def query(url):

    # url = 'https://www.cosdq.com/cosfl/'+str(page) +'.html'

    try:

        res = requests.get(url)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = 'body > div > div.content.pb20.clr > div.cy_cosCon > div.w.maxImg.tc > p > img'

        resurls = reslxml.select(selecter)

        return True, resurls

    except:

        return False, ''


def find(url):

    try:

        res = requests.get(url)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = 'body > div > div.content.hidden > ul.cy2-coslist.clr > li > div.showImg > a'

        resurls = reslxml.select(selecter)

        ret = []

        for x in resurls:

            urlcut = x.get('href')

            ret.append(urlcut)

        return True, ret

    except:

        return False, ''


def saveImage(resurls):

    try:
        i = 1

        maimpath = 'D:/IMAGES/'

        ffoldername = resurls[1].get('alt')

        foldername = str(ffoldername).replace('／', '')

        foldername = str(foldername).replace(':  ', '_')

        foldername = str(foldername).replace(' ', '_')

        fullpath = maimpath + foldername + '/'

        checked = os.path.exists(fullpath)

        if(not checked):

            os.makedirs(fullpath)

        ret = []

        for x in resurls:

            urlcut = x.get('src')

            if(urlcut == None):

                urlcut = x.get('data-loadsrc')

            ret.append(urlcut)

        for x in ret:

            print('正在保存：' + fullpath + str(i) + '.jpg')

            try:

                urllib.request.urlretrieve(x, fullpath + str(i) + '.jpg')

            except:
                x = 'https://t2cy.com/' + x

                urllib.request.urlretrieve(x, fullpath + str(i) + '.jpg')

            i += 1

        print('保存完成：'+foldername)

        return True, '保存成功'

    except:

        return True, '保存失败'


def main(index):

    print(index)

    url = 'https://t2cy.com/acg/cos/index.html'

    max = 5

    baseurl = 'https://t2cy.com/'

    while (index <= index + max):

        url = 'https://t2cy.com/acg/cos/index'+'_' + str(index) + '.html'

        if(index == 1):

            url = 'https://t2cy.com/acg/cos/index.html'

        checked, urls = find(url)

        for x in urls:

            url = baseurl + x

            checked, imgurls = query(url)

            checked, res = saveImage(imgurls)

            time.sleep(0.5)

        index += 1


def threadDomain():

    t1 = threading.Thread(target=main, args=(1,))
    t1.start()
    t2 = threading.Thread(target=main, args=(7,))
    t2.start()
    t3 = threading.Thread(target=main, args=(13,))
    t3.start()
    t4 = threading.Thread(target=main, args=(19,))
    t4.start()


threadDomain()
