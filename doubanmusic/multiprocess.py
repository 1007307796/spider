import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool

import datetime
starttime = datetime.datetime.now()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

def get_url_music(url):
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    aTags = soup.find_all("a",attrs={"class": "nbg"})
    for aTag in aTags:
        get_music_info(aTag['href'])


def get_music_info(url):

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
    print(info)

if __name__ == '__main__':
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0,100,25)]
    print(len(urls))
    pool = Pool(processes=4)
    pool.map(get_url_music,urls)