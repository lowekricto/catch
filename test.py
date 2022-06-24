
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

# 网站的URl
url = ''
# 标准header
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
}


# 服务器图片资源URL 可以是视频
imageurl = ''

# 保存到本地路径+文件名
fullpath = ''

proxies = {'http': 'http://127.0.0.1:1081', 'https': 'http://127.0.0.1:1081'}

# 使用代理进行get
res = requests.get(url, headers=header, proxies=proxies)
# 使用代理保存网络资源（图片and视频）
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
# 设置代理
opener.add_handler(urllib.request.ProxyHandler(proxies))
# opener.request.ProxyHandler(proxies)

urllib.request.install_opener(opener)

urllib.request.urlretrieve(imageurl, fullpath,)
