from pyquery import PyQuery as pq
import requests
import time
import xlwt
from src.funs import getheader
def get_one_page(url):
    try:
        headers = getheader('header.txt')
        result = requests.get(url,headers=headers)
        if result.status_code == 200:
            # 这样会乱码print(result.text)
            html = result.content
            html_doc = str(html, 'utf-8')
            return html_doc
        return None
    except Exception:
        return None

# 产生器
def parse_one_page(html):
    doc = pq(html)
    liList = doc('.gl-item')

    for li in liList.items():
        #items()方法将 liList转换为可迭代的PyQuery对象
        product = li('div > div.p-name.p-name-type-2 > a > em')[0].text
        exit('-------')
        if product == None:  # 京东精选
            product = li(' div > div.p-name.p-name-type-2 > a').attr('title')

        price = li('div > div.p-price > strong > i').text()
        seller = li('div > div.p-shop > span > a').text()
        yield {
            'product':product,
            'price':price,
            'seller':seller
        }


if __name__ == '__main__':
    order = 1
    urls = []
    for page in range(1,6,2):
        urlTop = 'https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&psort=3&wq=%E6%89%8B%E6%9C%BA' \
                 '&psort=3&page={}&s={}&click=0'.format(2*page-1,order)
        order+=30
        urls.append(urlTop)
        urlNext = 'https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&psort=3&wq=%E6%89%8B%E6%9C%BA&psort=3' \
                  '&page={}&s={}&scrolling=y&log_id=1596524438059.8672&tpl=3_M&isList=0&show_items='.format(2*page,order)
        urls.append(urlNext)
        order+=30
    header = ['排名','产品', '价格', '卖家']
    book = xlwt.Workbook(encoding='utf-8')
    sheet_all = book.add_sheet('所有手机销量排名')
    sheel_apple = book.add_sheet('Apple手机销量排名')
    sheel_huawei = book.add_sheet('华为手机销量排名')
    sheel_xiaomi = book.add_sheet('小米手机销量排名')
    for h in range(len(header)):
        sheet_all.write(0, h, header[h])
        sheel_apple.write(0, h, header[h])
        sheel_huawei.write(0, h, header[h])
        sheel_xiaomi.write(0, h, header[h])
    i = 1
    apple_i = 1
    huawei_i = 1
    xiaom_i = 1
    for url in urls[:1]:
        mobile_infos = parse_one_page(get_one_page(url))
        for mobile_info in mobile_infos:
            #print(mobile_info)
            sheet_all.write(i, 0, str(i))
            sheet_all.write(i, 1, mobile_info['product'])
            sheet_all.write(i, 2, mobile_info['price'])
            sheet_all.write(i, 3, mobile_info['seller'])
            if mobile_info['product'].lower().find('apple') != -1:
                sheel_apple.write(apple_i, 0, str(apple_i))
                sheel_apple.write(apple_i, 1, mobile_info['product'])
                sheel_apple.write(apple_i, 2, mobile_info['price'])
                sheel_apple.write(apple_i, 3, mobile_info['seller'])
                apple_i += 1
            if mobile_info['product'].lower().find('华为') != -1:
                sheel_huawei.write(huawei_i, 0, str(huawei_i))
                sheel_huawei.write(huawei_i, 1, mobile_info['product'])
                sheel_huawei.write(huawei_i, 2, mobile_info['price'])
                sheel_huawei.write(huawei_i, 3, mobile_info['seller'])
                huawei_i += 1
            if mobile_info['product'].lower().find('小米') != -1:
                sheel_xiaomi.write(xiaom_i, 0, str(xiaom_i))
                sheel_xiaomi.write(xiaom_i, 1, mobile_info['product'])
                sheel_xiaomi.write(xiaom_i, 2, mobile_info['price'])
                sheel_xiaomi.write(xiaom_i, 3, mobile_info['seller'])
                xiaom_i += 1
            time.sleep(0.1)
            i += 1

    book.save('mobile_rank.xls')