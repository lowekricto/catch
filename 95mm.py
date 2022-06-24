import os
import time
import urllib
from datetime import datetime
import threading

import requests
from bs4 import BeautifulSoup


def query(url, hearder):

    try:

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = 'body > main > div > div.row.no-gutters > div > div.post-content > div.post > div > p > a > img'

        resurls = reslxml.select(selecter)

        return True, resurls

    except:
        print(1)

        return False, ''


def getMaxpage(url, header):

    try:

        ret = ''

        res = requests.get(url, headers=header)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = 'body > main > div > div.row.no-gutters > div > h1'

        resurls = reslxml.select(selecter)

        pagestr = (str(resurls[0]).split('/')[1])[0:3]

        for x in pagestr:

            try:
                float(x)
                ret += x
            except:
                continue

        return True, ret

    except:

        return False, '0'


def saveImage(resurls, header, i):

    try:

        maimpath = 'D:/IMAGES3/'

        ffoldername = resurls[0].get('alt')

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

        # print(ret)

        for x in ret:

            print('正在保存：' + fullpath + str(i) + '.jpg')

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            try:

                urllib.request.urlretrieve(x, fullpath + str(i) + '.jpg')

            except:
                x = 'https://t2cy.com/' + x

                urllib.request.urlretrieve(x, fullpath + str(i) + '.jpg')

            i += 1

        print('保存完成：'+fullpath + str(i) + '.jpg')

        return True, '保存成功'

    except:

        return True, '保存失败'


def main(index):

    url = 'https://www.95mm.net/1/1.html'
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    }

    max = 5000

    while (index < index + max):

        url = 'https://www.95mm.net/' + str(index) + '/1.html'

        checked, maxpage = getMaxpage(url, header)

        for i in range(1, int(maxpage)+1):

            imageurl = 'https://www.95mm.net/' + \
                str(index) + '/'+str(i)+'.html'

            checked, imgurls = query(imageurl, header)

            checked, res = saveImage(imgurls, header, i)

            time.sleep(0.1)

        index += 1


def threadDomain():

    t1 = threading.Thread(target=main, args=(1,))
    t1.start()
    t2 = threading.Thread(target=main, args=(5001,))
    t2.start()
    t3 = threading.Thread(target=main, args=(10001,))
    t3.start()
    t4 = threading.Thread(target=main, args=(15001,))
    t4.start()
    t5 = threading.Thread(target=main, args=(20001,))
    t5.start()
    t6 = threading.Thread(target=main, args=(25001,))
    t6.start()


threadDomain()
