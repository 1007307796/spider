import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,stat
from selenium.webdriver import  ActionChains
import  io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
dir = 'C:\\Users\\lenovo\\Desktop\\pic\\'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(chrome_options = options)
#print(browser.page_source)
for i in range(1, 101):
    browser.get('https://www.91cp20.com/register')
    wait = WebDriverWait(browser, 10)
    img1finished = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'yidun_bg-img')))
    time.sleep(2)
    img1_src = img1finished.get_attribute('src')
    wait = WebDriverWait(browser, 10)
    img2finished = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'yidun_jigsaw')))
    time.sleep(2)
    img2_src = img2finished.get_attribute('src')
    print(img1_src)
    print(img2_src)
    r1 = requests.get(img1_src)
    path1 = dir + str(i) + '.jpg'
    with open(path1, 'wb') as f:
        f.write(r1.content)
        f.close()
    path2 = dir + str(i) + '_1' + '.jpg'
    r2 = requests.get(img2_src)
    with open(path2, 'wb') as f:
        f.write(r2.content)
        f.close()
