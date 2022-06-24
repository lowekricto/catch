import os
import time
import urllib
from datetime import datetime
import threading
from lxml import etree

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from requests.models import CaseInsensitiveDict


def query(url, header, session):

    # url = 'https://www.cosdq.com/cosfl/'+str(page) +'.html'

    try:

        res = session.get(url, headers=header, verify=False)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#primary-home > article > div.entry-content > p > img'

        resurls = reslxml.select(selecter)

        return True, resurls

    except:

        print("被锁定！！！")

        return False, ''


def getimagesUrl(reslxml):
    x = 1

    max = 24

    ret = []

    while x <= 24:

        href = '/html/body/div/div[2]/div[2]/div/div[1]/div/ul/li[' + \
            str(x)+']/div/div[2]/h2/a/@href'

        title = '/html/body/div/div[2]/div[2]/div/div[1]/div/ul/li[' + \
            str(x)+']/div/div[2]/h2/a/text()'

        rehref = (reslxml.xpath(href))[0]

        retitle = (reslxml.xpath(title))[0]

        ret.append([retitle, rehref])

        x += 1

    return ret


def find(url, header, session):

    try:
        locked = True

        while locked:

            res = session.get(url, headers=header, verify=False)

            print(res)

            if(str(res) == '<Response [404]>'):
                time.sleep(10)
            else:
                locked = False

        res.encoding = 'utf-8'

        reslxml = etree.HTML(res.text)

        ret = getimagesUrl(reslxml)

        return True, ret

    except:

        return False, ''


def saveImage(resurls, foldName, header, session, basePath):

    try:
        i = 1

        maimpath = 'D:/IMAGES2/'+basePath

        fullpath = maimpath + foldName + '/'

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

            filename = fullpath + str(i) + '.jpg'

            session.headers.update(header)

            images = session.get(url=x)

            if(str(images) != '<Response [200]>'):
                continue

            with open(filename, 'wb') as file:
                file.write(images.content)

            i += 1

        print('保存完成：'+foldName)

        return True, '保存成功'

    except:

        return True, '保存失败'


def getphoto(index):

    basePath = 'photo/'

    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LmNvc2ppYW5nLmNvbSIsImlhdCI6MTYzMTE3NzMxNSwibmJmIjoxNjMxMTc3MzE1LCJleHAiOjE2MzE3ODIxMTUsImRhdGEiOnsidXNlciI6eyJpZCI6IjQ2MjQxIn19fQ.lkuQA2TGk6WqkA5LSl4NpcVVLREXVD96r1cFWsafgak',
        'cookie': 'wordpress_logged_in_7f0324c19139fd5a4000b16805f2a60f=user46241_702|1632375343|hoz2X2Oz5zH0QwqLSrmcdKVW2kNqawHo4wlf8fJIaxv|ebc9984451b0a2dcf2692debd67ee18d800d1d0de1c702b6a24cdffa5323de39; wfwaf-authcookie-e5400ce3ed19563b91b3e80ae0da0377=46241|subscriber|44a32d7d9b55aa011fdabdb2753ab9eb0fc127a73d018185d2cbdfa97b67072a',
        'if-modified-since': 'Wed, 08 Sep 2021 07:32:48 GMT',
        'if-None-Match': '"61386720-38f94"',
        'contebt-length': 234,
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.cosjiang.com',
        'referer': 'https://www.cosjiang.com/cosplay',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',

    }
    session = requests.session()
    requests.packages.urllib3.disable_warnings()

    url = 'https://www.cosjiang.com/photo'

    max = 81

    baseurl = 'https://t2cy.com/'

    while (index <= max):

        print(index)

        url = 'https://www.cosjiang.com/photo/'+'page/' + str(index)

        if(index == 1):

            url = 'https://www.cosjiang.com/photo'

        checked, urls = find(url, header, session)

        for x in urls:

            foldName = x[0]
            url = x[1]

            locked = True

            while locked:

                checked, imgurls = query(url, header, session)

                if(checked):

                    locked = False
                else:

                    print('photo被锁定等待15S')
                    locked = True
                    time.sleep(15)

            header['referer'] = url

            checked, res = saveImage(
                imgurls, foldName, header, session, basePath)

            time.sleep(0.2)

        index += 1


def getcoser(index):

    basePath = 'cosplay/'
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'wordpress_logged_in_7f0324c19139fd5a4000b16805f2a60f=user46241_702|1632375343|hoz2X2Oz5zH0QwqLSrmcdKVW2kNqawHo4wlf8fJIaxv|ebc9984451b0a2dcf2692debd67ee18d800d1d0de1c702b6a24cdffa5323de39; wfwaf-authcookie-e5400ce3ed19563b91b3e80ae0da0377=46241|subscriber|44a32d7d9b55aa011fdabdb2753ab9eb0fc127a73d018185d2cbdfa97b67072a',
        'if-modified-since': 'Wed, 08 Sep 2021 07:32:48 GMT',
        'if-None-Match': '"61386720-38f94"',
        'referer': '',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',

    }
    session = requests.session()
    requests.packages.urllib3.disable_warnings()

    url = 'https://www.cosjiang.com/cosplay'

    max = 58

    baseurl = 'https://t2cy.com/'

    while (index <= max):

        print(index)

        url = 'https://www.cosjiang.com/cosplay/'+'page/' + str(index)

        if(index == 1):

            url = 'https://www.cosjiang.com/cosplay'

        checked, urls = find(url, header, session)

        for x in urls:

            foldName = x[0]
            url = x[1]

            locked = True

            while locked:

                checked, imgurls = query(url, header, session)

                if(checked):

                    locked = False
                else:

                    print('coser被锁定等待15S')
                    locked = True
                    time.sleep(15)

            header['referer'] = url

            checked, res = saveImage(
                imgurls, foldName, header, session, basePath)

            time.sleep(0.2)

        index += 1
        break


def main():
    getphoto(1)


main()
