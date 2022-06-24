import os
import time
import urllib
from io import BytesIO
from PIL import Image
from urllib.parse import quote

from datetime import datetime
import json
import threading

import requests
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:1081', 'https': 'http://127.0.0.1:1081'}


def getcosers(header):

    try:
        url = 'https://zfile.cosersets.com/api/list/1?path=%2F&password=&orderBy=&orderDirection='

        res = requests.get(url, headers=header, proxies=proxies)

        cosers = json.loads(res.text)

        ret = []

        for x in (cosers['data'])['files']:
            ret.append(x['name'])

        return ret

    except:
        return []


def getcoserWorks(coser, header, url_copy):

    try:
        url = 'https://zfile.cosersets.com/api/list/1?path=%2F' + \
            coser+'&password=&orderBy=&orderDirection='

        res = requests.get(url, headers=header, proxies=proxies)

        cosers = json.loads(res.text)

        ret = []

        for x in (cosers['data'])['files']:
            ret.append([x['name'], x['type'], x['url'], x['path']])

        imageurls = []

        for y in ret:

            if(y[1] == "FOLDER"):

                getcoserWorks(url_copy + y[0], header, url_copy + y[0])

            else:

                imageurls.append([y[3], str(y[2]).replace(' ', '%20'), y[0]])

        ret = saveImage(imageurls)

        return ret
    except:
        return []


def getimages(coser, header):

    try:
        url = 'https://zfile.cosersets.com/api/list/1?path=%2F' + \
            coser+'&password=&orderBy=&orderDirection='

        res = requests.get(url, headers=header, proxies=proxies)

        cosers = json.loads(res.text)

        ret = []

        for x in (cosers['data'])['files']:

            ret.append(
                [x['path'], str(x['url']).replace(' ', '%20'), x['name']])

        return ret
    except:
        return []


def webp2jpg(folderpath, image):
    try:
        imagename = (str(image).split('.'))[0]

        im = Image.open(folderpath+image).convert("RGB")

        im.save(folderpath+imagename+'.jpg', 'JPEG', quality=100)

        os.remove(folderpath+image)
    except:
        print(folderpath+image+"不存在！")


def saveImage(imageurls):

    try:
        i = 1

        # maimpath = '/home/kricto/A_ACGN/M_萌小寒图包/L_【杂图】/C_【coserset】'
        maimpath = 'Z:\A_ACGN\L_LSP'

        t = threading.currentThread()
        tname = t.getName()

        for x in imageurls:

            fullpath = maimpath + x[0]
            checked = os.path.exists(fullpath)

            if(not checked):

                os.makedirs(fullpath)

            imagename = (str(x[2]).split('.'))[0]
            checked = os.path.exists(fullpath+imagename+'.jpg')
            checked2 = os.path.exists(fullpath+imagename+'.mp4')

            if(checked | checked2):
                continue
            print(tname+'=> 正在保存：' + fullpath + x[2])

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            # 设置代理
            opener.add_handler(urllib.request.ProxyHandler(proxies))
            # opener.request.ProxyHandler(proxies)

            urllib.request.install_opener(opener)

            try:
                imageurl = quote(x[1], safe='/:?=%')

                urllib.request.urlretrieve(imageurl, fullpath + x[2],)

                webp2jpg(fullpath, x[2])

            except:
                print(tname+'=> 保存失败：'+x[0])

            i += 1

        print(tname+'=> 保存完成：'+x[0])

        return True, '保存成功'

    except:

        return True, '保存失败'


def thread(cosers, header):

    for coser in cosers:
        url_copy = '/' + coser + '/'

        workslist = getcoserWorks(coser, header, url_copy)

    t = threading.currentThread()
    tname = t.getName()
    print('##########################################'+tname +
          '执行完毕了#####################################################')


def sendThread(cosers):
    ret = []
    temp = []

    for x in cosers:
        temp.append(x)
        if(temp.__len__() == 1):
            ret.append(temp)
            temp = []
    return ret


def makethreadPool(index):
    ret = []
    for x in range(0, index):
        print(x)


def remakethread(new, old):
    ret = new

    for x in old:
        ret.append([x])
    return ret


def main():

    url = 'https://www.cosersets.com/1/main/'

    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    }

    cosers = getcosers(header)

    cosers = sendThread(cosers)

    for coser in cosers:
        t = threading.Thread(target=thread, args=(coser, header))
        t.start()


main()
