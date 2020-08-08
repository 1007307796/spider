# -coding:utf8-
import time
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support import ui
from scrapy.http import HtmlResponse

url = 'https://www.kaishiba.com/project/more.html'
browser = webdriver.Chrome()

try:
    browser.get(url)
    wait = ui.WebDriverWait(browser, 20)   # 等待20秒加载driver，要么执行方法，要么抛出异常
    wait.until(lambda dr: dr.find_element_by_class_name('project-detail').is_displayed())
    # 由于project-detail标签在末尾，要等待数据加载完毕才执行返回response
    # 反复调用wait方法直到为真
    # until():Calls the method provided with the driver as an argument until the return value is not False.
    # lambda匿名函数：如lambda x: x+2形式
    # is_displayed()：元素是否存在页面上，包括不可见，若存在返回真，反之为假
    js1 = 'return document.body.scrollHeight'
    js2 = 'window.scrollTo(0, document.body.scrollHeight)'
    old_scroll_height = 0
    while browser.execute_script(js1) >= old_scroll_height:
        old_scroll_height = browser.execute_script(js1)
        browser.execute_script(js2)
        time.sleep(1)
        break
    sel = Selector(text=browser.page_source)
    proj_list = sel.xpath('//span[@class="author"]/text()').extract()   # page_source得到当前页面的来源

    for i in proj_list:
        print(i)
finally:
    browser.quit()


