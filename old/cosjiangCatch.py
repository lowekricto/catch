import os
import time
import urllib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from requests.models import CaseInsensitiveDict


def find(page):

    # url = 'https://www.cosdq.com/cosfl/'+str(page) +'.html'

    try:

        url = 'https://t2cy.com/acg/cos/cosplay/'+ page +'.html'

        res = requests.get(url)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text,'lxml')

        selecterError = 'body > div > div > img'

        resurls = reslxml.select(selecterError)

        print(resurls)

        if(resurls.__len__() != 0):

            return False,'页面不存在已经跳过'

        selecter = 'body > div > div.content.pb20.clr > div.cy_cosCon > div.w.maxImg.tc > p > img'

        resurls = reslxml.select(selecter)
    
        return True, resurls
    
    except:
        
        return False,''

    


def saveImage(resurls,flpage):

    try:
        i = 1

        maimpath = 'D:/IMAGES/'

        ffoldername = resurls[1].get('alt')

        foldername = str(ffoldername).replace('／','')

        foldername = str(foldername).replace(':  ','_')

        foldername = str(foldername).replace(' ','_')

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
        
        return True,'保存成功'

    except:
        
        return True, flpage + '保存失败'
    
    


    

def addDate(date):
    
    let = date

    transDate = datetime.strptime(let,"%Y-%m-%d").date()

    addoneday = transDate + relativedelta(days=1)

    ret = str(addoneday)

    return ret





def main():

    flpage = 210

    # maxFLpage = 82

    maxFLpage = 1315

    addsize = 1
    
    maxaddsize = 20

    date = '2018-04-04'

    while True:

        if ( flpage == maxFLpage ):
            
            break

        fullpage = date + '/' + str(flpage)

        print('当前页码：' + str(fullpage) )

        try:

            checked,resurls = find(fullpage)

            if( not checked):

                print(resurls)

                addsize += 1

                flpage += 1
                
                if(addsize == maxaddsize):

                    addsize = 1

                    flpage = flpage - maxaddsize

                    flpage += 1
                    
                    date = addDate(date)
                
                time.sleep(0.1)

                continue

            addsize = 1
            

            checked,res = saveImage(resurls,fullpage)

            if( not checked ):

                print(res)

            flpage += 1

            time.sleep(0.2)
        
        except:
        
            flpage += 1

main()
