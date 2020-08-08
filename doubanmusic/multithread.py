import threading
import datetime
import requests
from bs4 import BeautifulSoup
import re
import time

starttime = datetime.datetime.now()

lock = threading.Lock()
def get_url():
    global urls
    lock.acquire()
    if len(urls) == 0:
        lock.release()
        return ""
    else:
        url = urls[0]
        del urls[0]
    lock.release()
    return url



print(time.time())
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

def get_url_music(url,thread_name):
    html = requests.get(url,headers=headers)

    soup = BeautifulSoup(html.text, 'lxml')

    aTags = soup.find_all("a",attrs={"class": "nbg"})
    for aTag in aTags:
        get_music_info(aTag['href'],thread_name)


def get_music_info(url,thread_name):
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.find (attrs={'id':'wrapper'}).h1.span.text
    author = soup.find(attrs={'id':'info'}).find('a').text
    styles = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />', html.text, re.S)
    if len(styles) == 0:
        style = '未知'
    else:

        style = styles[0].strip()
    time = re.findall('发行时间:</span>&nbsp;(.*?)<br />', html.text, re.S)[0].strip()
    publishers = re.findall('<span class="pl">出版者:</span>&nbsp;(.*?)<br />', html.text, re.S)
    if len(publishers) == 0:
        publisher = '未知'
    else:
        publisher = publishers[0].strip()


    score = soup.find(class_='ll rating_num').text
    info = {
        'name': name,
        'author': author,
        'style': style,
        'time': time,
        'publisher': publisher,
        'score': score
    }
    print(thread_name, info)
class SpiderThread (threading.Thread):   #继承父类threading.Thread

    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        while True:
            url = get_url()
            if url != "":
                get_url_music(url,self.name)
            else:
                break


if __name__ == '__main__':
    url_index = 0
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0,100,25)]
    print(len(urls))
    # 创建新线程
    thread1 = SpiderThread('thread1')
    thread2 = SpiderThread('thread2')
    thread3 = SpiderThread('thread3')
    thread4 = SpiderThread('thread4')

    # 开启线程
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    print("退出爬虫")
    endtime = datetime.datetime.now()
    print('需要时间：',(endtime - starttime).seconds,'秒')

