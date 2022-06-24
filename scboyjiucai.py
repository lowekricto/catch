import os
from telnetlib import TM
import time
import urllib
from datetime import datetime
import threading
from lxml import etree

import datetime
import requests
from bs4 import BeautifulSoup


def do():
    header = {
        "cookie": "bbs_token=P62jCVsWr9504BF_2F7Iq0cjSsOikTV423qIdkfuTJlXEg_2Fp0eE4MD3MHQ6nw_2Fzk_2FBTyw8_2FxFV5iulMqNjAcyOzA_3D_3D; bbs_sid=458013c9035834363c49487a843e3def; UM_distinctid=17c7c5991345db-070396d0205a9e-513c1e45-32a000-17c7c59913583f; atarget=n; CNZZDATA1277689586=267366360-1634168641-|1637406544",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
    }
    session = requests.session()
    requests.packages.urllib3.disable_warnings()

    url = "https://www.scboy.cc/?thread-316509.htm"

    res = session.get(url, headers=header, verify=False)

    res.encoding = 'utf-8'

    reslxml = BeautifulSoup(res.text, 'lxml')

    selecter1 = '#body > div > div > div.col-lg-9.main > div.mt-3.haya-poll-thread-poll > div.card > div.m-3 > div.mt-3.haya-poll-thread-poll-content > div > div > div:nth-child(1) > div:nth-child(1)'

    selecter2 = '#body > div > div > div.col-lg-9.main > div.mt-3.haya-poll-thread-poll > div.card > div.m-3 > div.mt-3.haya-poll-thread-poll-content > div > div > div:nth-child(2) > div:nth-child(1)'

    selected1 = reslxml.select(selecter1)

    selected2 = reslxml.select(selecter2)

    text1 = str(selected1[0].text)

    text2 = str(selected2[0].text)

    print('******************************************************************************')

    print(datetime.datetime.now())

    print(text1)

    print(text2)

    print('******************************************************************************')


while True:
    do()
    time.sleep(5)
