import os

import threading
import time
import urllib
from datetime import datetime
from urllib.parse import quote

import requests

from bs4 import BeautifulSoup


def query(url, hearder):

    ret = []

    try:

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#wrap > div > main > section > div.sec-panel-body > ul.post-loop.post-loop-image.cols-4 > li > div > h2 > a'

        resurls = reslxml.select(selecter)

        for x in resurls:

            username = str(x.text)
            username = username.replace("\n", "")
            username = username.replace("\t", "")
            username = username.replace("\r", "")
            username = username.replace(" ", "")

            herf = x.get('href')

            ret.append([username, herf])

        return True, ret

    except:
        print(1)

        return False, ''


def getimages(url, header):

    try:

        ret = []

        urlname = (url.split('.')[1]).split('/')[-1]

        res = requests.get(url, headers=header)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#post-'+urlname + \
            ' > div.entry-main > div.entry-content.text-indent > figure >img'

        resurls = reslxml.select(selecter)

        index = 0

        for x in resurls:
            index += 1
            name = str(index).rjust(2, "0") + '.jpg'
            src = x.get('data-original')

            ret.append([name, src])

        return True, ret

    except:

        return False, '0'


def saveimages(images, foldername):

    try:
        # maimpath = 'Z:\A_ACGN\L_LSP'
        maimpath = 'D:\IMAGES5'
        # maimpath = '/KALOS/T_Tmp/IMAGES'

        t = threading.currentThread()
        tname = t.getName()

        for x in images:

            name = x[0]
            src = x[1]

            fullpath = maimpath + '\\' + foldername + '\\'
            checked = os.path.exists(fullpath)

            if(not checked):

                os.makedirs(fullpath)

            checked = os.path.exists(fullpath+name)
            if(checked):
                continue
            print(tname+'=> 正在保存：' + fullpath + name)

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            try:
                imageurl = quote(src, safe='/:?=%')

                urllib.request.urlretrieve(
                    imageurl, fullpath + name)

            except:
                print(tname+'=> 保存失败：'+fullpath + name)

        print(tname+'=> 保存完成：'+foldername)
        return True, '保存成功'
    except:
        return True, '保存失败'


def main(i):

    for index in i:
        url = 'https://dongtidemi.com/category/tu/%E7%A6%8F%E5%88%A9%E5%A7%AC/page/' + \
            str(index)
        header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
        }
        checked, queryret = query(url, header)
        for x in queryret:
            username = x[0]
            herf = x[1]
            checked, images = getimages(herf, header)
            if(checked):
                saveimages(images, username)


# def sendThread(cosers):
#     ret = []
#     temp = []

#     for x in cosers:
#         temp.append(x)
#         if(temp.__len__() == 29):
#             ret.append(temp)
#             temp = []
#     return ret

cosers = []

for x in range(1, 291):
    cosers.append(x)


main(cosers)

# cosers = sendThread(cosers)

# for x in cosers:
#     threading.Thread(target=main, args=(x,)).start()
