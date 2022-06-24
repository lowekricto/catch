import os
import time
import urllib
from datetime import datetime
import threading
from lxml import etree

import requests

from requests.models import CaseInsensitiveDict


def find(url, hearder):

    try:
        x = 1
        resurls = []

        res = requests.get(url, headers=hearder)

        res.encoding = "utf-8"

        reslxml = etree.HTML(res.text)
        while x <= 12:

            hrefs = (
                "/html/body/div[1]/div[1]/div["
                + str(x)
                + "]/article/div/figure/a/@href"
            )
            names = (
                "/html/body/div[1]/div[1]/div["
                + str(x)
                + "]/article/div/figure/a/figcaption/text()"
            )

            rethrefs = reslxml.xpath(hrefs)[0]
            retnames = reslxml.xpath(names)[0]

            resurls.append([retnames, rethrefs])

            x += 1

        return True, resurls

    except:
        print(url + "URL不存在")

        return False, ""


def query(url, hearder):

    # url = 'https://www.cosdq.com/cosfl/'+str(page) +'.html'
    resurls = []
    try:

        x = 1

        res = requests.get(url, headers=hearder)

        res.encoding = "utf-8"

        reslxml = etree.HTML(res.text)

        try:

            while x < 999:

                hrefs = (
                    "/html/body/div[1]/div/figure[" +
                    str(x) + "]/a/img/@data-original"
                )

                rethrefs = reslxml.xpath(hrefs)[0]

                resurls.append(rethrefs)

                x += 1
        except:
            return True, resurls
        return True, resurls

    except:

        print("被锁定！！！")

        return False, ""


def doSave(x, fullpath, i):
    opener = urllib.request.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36",
        )
    ]
    urllib.request.install_opener(opener)

    try:
        t = threading.Thread(
            target=urllib.request.urlretrieve,
            args=(
                x,
                fullpath + str(i) + ".jpg",
            ),
        )

        t.setDaemon(True)
        t.start()
        alive = 0
        while t.is_alive():
            time.sleep(1)
            alive += 1
            if alive == 300:
                print("保存失败"+fullpath + str(i) + ".jpg")
                return

    except:
        print("保存失败"+fullpath + str(i) + ".jpg")


def saveImage(folder, urls, header, minpage, maxpage, x):

    try:

        maimpath = "/home/kricto/data/A_ACGN/M_萌小寒图包/L_【杂图】/X_【新美图录】/J_【日本】/【page】[" + str(
            minpage)+"-"+str(maxpage)+']/【page】['+str(x)+']/'
        # maimpath = "D:/IMAGES5/"

        ffoldername = folder

        foldername = str(ffoldername).replace("／", "")

        foldername = str(foldername).replace(":  ", "_")

        foldername = str(foldername).replace(" ", "_")

        fullpath = maimpath + foldername + "/"

        checked = os.path.exists(fullpath)

        if not checked:

            os.makedirs(fullpath)

        # print(ret)
        i = 0

        for x in urls:
            i += 1

            checked = os.path.exists(fullpath + str(i) + ".jpg")
            if checked:

                continue

            print("正在保存：" + fullpath + str(i) + ".jpg")

            doSave(x, fullpath, i)

        return True, "保存成功"

    except:

        return True, "保存失败"


def main(index):
    # 1-20
    for x in range((120 * index) - 119, 120 * index):

        try:
            url = "https://www.xinmeitulu.com/area/ribenmeinyu/page/" + \
                str(x)

            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
            }

            checked, pages = find(url, header)

            for urls in pages:
                name = urls[0]
                singleurl = urls[1]
                checked, imageUrls = query(singleurl, header)
                saveImage(name, imageUrls, header,
                          (120 * index)-119, (120 * index), x)
        except:
            continue
        print('第'+str(x)+"页保存完成")


def thread(index):
    for x in range(1, index + 1):
        t1 = threading.Thread(target=main, args=(x,))
        t1.start()


thread(20)
