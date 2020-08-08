from selenium import webdriver
import time
import os
from src.funs import webDriver_wait

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#进程过多时运行
#os.system('taskkill /im chrome.exe /F')
#os.system('taskkill /im chromedriver.exe /F')
browser = webdriver.Chrome('chromedriver')

def get_info(qq):
    #若设置无头，这里必须写完整url
    browser.get('https://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(2)
    browser.switch_to.frame('login_frame')
    browser.find_element_by_id('switcher_plogin').click()
    browser.find_element_by_id('u').clear()
    browser.find_element_by_id('u').send_keys(qq)
    browser.find_element_by_id('p').clear()
    browser.find_element_by_id('p').send_keys('**********')
    login = browser.title
    browser.find_element_by_id('login_button').click()
    while browser.title == login:
        # TODO:滑动验证码
        time.sleep(3)
    time.sleep(3)
    wait_frame = 'app_canvas_frame'
    browser.switch_to.frame(wait_frame)
    wait_datas = 'content'
    has_data = True
    while has_data:
        isGet = webDriver_wait(wait_datas, browser, 1)
        if isGet == True:
            contents = browser.find_elements_by_css_selector('.content')
            times = browser.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
            for content, tim in zip(contents, times):
                data = {
                    'time': tim.text,
                    'content': content.text
                }
                print(data)
            try:
                nextPage = browser.find_element_by_css_selector('.mod_pagenav_main > a:last-child')
                title = nextPage.get_attribute('title')
                if title == '下一页':
                    nextPage.click()
                    print('正在获取下一页...')
                    for i in range(5):
                        browser.execute_script('window.scrollBy(0,document.body.scrollHeight)')
                        time.sleep(1)
            except:
                print('所有数据获取完成')
                has_data = False
        else:
            print('请求超时或未找到该节点')
    #browser.quit()

if __name__ == '__main__':
    try:
        get_info('1984759093')
    except Exception as e:
        print(e)
        browser.quit()

