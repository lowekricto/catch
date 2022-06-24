import os
import time
import urllib

import requests
from bs4 import BeautifulSoup

# maimpath = 'D:/IMAGES/'

# url = 'https://www.cosdq.com/cosfl/1292.html'

# res = requests.get(url)

# reslxml = BeautifulSoup(res.text,'lxml')

# # selecter = 'body > div > div.cont.cf > div.m_l > div.b1_top > div > div.content > p'

# selecter = 'body > div > div.cont.cf > div.m_l > div.b1_top > div > div.content > p > img'

# resurls = reslxml.select(selecter)

# ret = []

# for x in resurls:

#     urlcut = x.get('src')
    
#     ret.append(urlcut)

# # x = 'https://www.cosdq.com/upload/article/202108/23/111710612313360b9ddE8XHc2.jpg'

# # urllib.request.urlretrieve(x,'D:/IMAGES/1.jpg')

# # for x in ret:
# #     urllib.request.urlretrieve(x,'D:/IMAGES/')


# print(resurls)


def find(page):

    url = 'https://www.cosdq.com/cosfl/'+str(page) +'.html'

    res = requests.get(url)

    reslxml = BeautifulSoup(res.text,'lxml')

    # selecter = 'body > div > div.cont.cf > div.m_l > div.b1_top > div > div.content > p'

    selecter = 'body > div > div.cont.cf > div.m_l > div.b1_top > div > div.content > p > img'

    resurls = reslxml.select(selecter)
    
    return resurls


def saveImage(resurls):
    
    i = 1

    maimpath = 'D:/IMAGES2/'

    foldername = resurls[0].get('alt')

    fullpath = maimpath + foldername +'/'

    checked =os.path.exists(fullpath)

    if( not checked ):

        os.makedirs(fullpath)

    ret = []

    for x in resurls:

        urlcut = x.get('src')
    
        ret.append(urlcut)

    for x in ret:

        urllib.request.urlretrieve(x,fullpath + str(i) +'.jpg')
        
        i += 1


    # print(resurls)


def main():

    # flpage = 1291

    # maxFLpage = 1292

    bzpage = 13

    maxBZpage = 692

    flpage = bzpage

    maxFLpage = maxBZpage

    while True:

        if ( flpage == maxFLpage ):
            
            break

        time.sleep(0.2)

        print('当前页码：' + str(flpage) )

        try:

            resurls = find(flpage)

            saveImage(resurls)

            flpage += 1
        
        except:
        
            flpage += 1

main()
