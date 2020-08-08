# -*- coding: utf-8 -*-
from selenium import webdriver
import csv
from selenium.webdriver.chrome.options import Options

url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'
# 初始爬取网址
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')   # 添加Chrome初始化设置（这里设置禁用GUI和禁用GPU）
driver = webdriver.Chrome(chrome_options=chrome_options)   # 用Chrome接口创建一个selenium的webDriver
csv_file = open("playlist.csv", "w", newline='', encoding='utf-8')  # newline:在清空Windows缓存区的换行/以相符的编码格式打开
writer = csv.writer(csv_file)
writer.writerow(['标题', '播放数', '链接'])
# 初始化csv存储文件
j = 1
while url != 'javascript:void(0)':   # 当下一页的值不为空的时候
    driver.get(url)   # 用webdriver代开页面
    driver.switch_to.frame("contentFrame")   # 切换到目标所在的框架
    data = driver.find_element_by_id("m-pl-container").find_elements_by_tag_name("li")
    # 定位目标标签
    for i in range(len(data)):   # 解析一页中的歌单信息
        nb = data[i].find_element_by_class_name("nb").text
        if '万' in nb and int(nb.split("万")[0]) > 500:
            cover = data[i].find_element_by_css_selector("a.msk")
            writer.writerow([cover.get_attribute('title'), nb, cover.get_attribute('href')])
    print('正在下载第' + str(j) + '页')
    j = j + 1
    # 定位下一页的url
    url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute('href')
csv_file.close()


