import os
import time
import urllib
from datetime import datetime
import threading

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素


import requests
from bs4 import BeautifulSoup

desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
# 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
desired_capabilities["pageLoadStrategy"] = "none"


# 任务数
TASK_ALL = 0
TASK_NOW = 0
TASK_FINISH = 0

# 线程数
THREAD_MAX = 10
THREAD_RUNN = 0

#
lock = threading.Lock()

# 任务列表
TASK_LIST = []


HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
}


URL_BASE = 'https://www.sakuradm.tv'
URL_SEARCH_BASE = 'https://www.sakuradm.tv/vodsearch.html?wd='
###########################################################################################
# 工具


def taskstart():
    global TASK_ALL, TASK_NOW, THREAD_RUNN

    TASK_NOW += 1
    THREAD_RUNN += 1


def taskFinish():
    global TASK_ALL, TASK_NOW, TASK_FINISH
    global THREAD_RUNN
    TASK_NOW -= 1
    TASK_FINISH += 1
    THREAD_RUNN -= 1


def nowtask():
    global TASK_ALL, TASK_NOW, TASK_FINISH
    print('正在进行的任务数：'+str(TASK_NOW))
    print('全部的任务数：'+str(TASK_ALL))
    print('已完成的任务数：'+str(TASK_FINISH))


def getatask():
    global TASK_LIST

    ret = []

    lock.acquire()

    ret = TASK_LIST[0]
    del TASK_LIST[0]

    lock.release()

    return ret


def threadSave():
    task = getatask()
    url = task[0]
    path = task[1]
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, path)
    taskFinish()
    print(path+'保存完毕')


def threadSend():
    global THREAD_RUNN, THREAD_MAX, TASK_LIST
    print('Mession Pool flow')

    while(1):

        count = getcount(TASK_LIST)

        if(count == 0):

            time.sleep(1)
            continue

        if(THREAD_RUNN <= THREAD_MAX):
            # 开启新线程
            taskstart()
            t = threading.Thread(target=threadSave, args=())
            t.start()


def doinput():
    inputs = input("Enter your input: ")

    if(inputs == 'top'):
        nowtask()
        return ''

    strs = str(inputs)

    return strs


def selectinput():
    inputs = input("Enter your input: ")

    strs = str(inputs)

    print('确认到输入的动漫名为：'+strs)

    return strs


def getcount(list):
    index = 0
    for x in list:
        index += 1
    return index


def linkurlandname(urls, names):
    ret = []
    temUrl = []
    temName = []

    lengths = 0

    for x in urls:
        lengths += 1
        temUrl.append(URL_BASE+str(x.get('href')))

    for y in names:
        temName.append(str(y.get('alt')))

    for z in range(0, lengths):
        ret.append([temName[z], temUrl[z]])

    return ret


def selectView(list):
    no = 0
    name = '我全都要'
    print('['+str(no)+'] '+name)
    for x in list:
        no += 1
        name = x[0]
        print('['+str(no)+'] '+name)
    print('[-1] 取消搜索')


############################################################################################
def query(url, hearder):

    try:

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#contrainer > div.fire.l > div.pics > ul > li > a'

        resurls = reslxml.select(selecter)

        if(resurls.count == 0):
            return False, []

        urlSelect = '#contrainer > div.fire.l > div.pics > ul > li > a'

        nameSelect = '#contrainer > div.fire.l > div.pics > ul > li > a > img'

        urlResurls = reslxml.select(urlSelect)

        nameResurls = reslxml.select(nameSelect)

        animes = linkurlandname(urlResurls, nameResurls)

        return True, animes

    except:
        print(1)

        return False, []


def queryvideos(url, hearder):

    try:
        ret = []

        res = requests.get(url, headers=hearder)

        res.encoding = 'utf-8'

        reslxml = BeautifulSoup(res.text, 'lxml')

        selecter = '#play_1 > ul > li > a'

        resurls = reslxml.select(selecter)

        for x in resurls:
            ret.append([x.text, URL_BASE+str(x.get('href'))])

        return True, ret

    except:
        print(1)

        return False, []


def queryvideosurls(url, hearder, browser):

    try:
        ret = []
        browser.get(url)
        # browser.implicitly_wait(2000)
        time.sleep(3)
        iframe = browser.find_elements_by_tag_name("iframe")[2]
        browser.switch_to.frame(iframe)

        selecter = '#player > div.yzmplayer-video-wrap > video'
        resurls = browser.find_elements_by_css_selector(selecter)
        videourl = resurls[0].get_attribute('src')

        return True, videourl

    except:
        print(1)

        return False, []


def search(name):
    url = URL_SEARCH_BASE+name

    checked, animes = query(url, HEADER)

    animeCount = getcount(animes)

    return animeCount, animes


def mp4Save(animepara, videosurls):

    global TASK_LIST, TASK_ALL

    maimpath = 'D:/ANIME/'

    ffoldername = animepara[0]
    foldername = str(ffoldername).replace('／', '')
    foldername = str(foldername).replace(':  ', '_')
    foldername = str(foldername).replace(' ', '_')
    fullpath = maimpath+foldername + '/'
    checked = os.path.exists(fullpath)

    if(not checked):
        os.makedirs(fullpath)

    # 保存
    for x in videosurls:

        TASK_LIST.append([x[1], fullpath + str(x[0]) + '.mp4'])
        TASK_ALL += 1

    print(ffoldername+'后台静默保存中')


def DoSingleAnimeSave(animepara):
    print('选择：'+animepara[0])
    browser = webdriver.Chrome()

    # 进入动漫页
    checked, videospage = queryvideos(animepara[1], HEADER)

    if(not checked):
        return False
    videosurls = []
    # URL 组装
    for x in videospage:
        checked, res = queryvideosurls(x[1], HEADER, browser)
        if(not checked):
            continue
        videosurls.append([x[0], res])
    browser.close()
    # 保存
    mp4Save(animepara, videosurls)


def main():

    t = threading.Thread(target=threadSend, args=())
    t.start()

    while(1):
        # 输入
        animeName = doinput()
        if(animeName == ''):
            continue
        print('确认到输入的动漫名为：'+animeName)

        counts, animes = search(animeName)

        if(counts == 0):
            print('查询的动漫不存在')
            continue
        elif(counts > 1):
            print('查询到多部请输入序号单个选择或者输入0选择全部：')
            selectView(animes)
            selected = input("Enter your input:")
        elif(counts == 1):
            selected = 1

        if(selected == '-1'):
            print('取消搜索')
            continue

        if(selected != '0'):
            selectanime = int(selected)-1
            animepara = animes[selectanime]
            # 单个动漫保存
            DoSingleAnimeSave(animepara)

            continue
        # 全部保存
        for x in animes:
            DoSingleAnimeSave(x)


main()
