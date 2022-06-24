# /html/body/main/article/div[2]/div[2]/div[2]/div[1]/video/@src

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


def find(url):

    try:

        print(url)

        res = requests.get(url)

        reslxml = etree.HTML(res.text)

        videoPath = '/html/body/main/article/div[2]/div[2]/div[2]/div[1]'

        videoSrc = reslxml.xpath(videoPath)

        print(videoSrc)

        return True

    except:

        return False, ''


def main(index):

    print(index)

    url = 'https://ddrk.me/hakozume/?ep=1'

    max = 7

    while (index <= index + max):

        url = 'https://ddrk.me/hakozume/?ep='+str(index) + '.html'

        checked = find(url)

        break


main(1)
