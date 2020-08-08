from pyquery import PyQuery as pq
from src.Cookie import write_to_xls
import requests


def get_one_page(url):
    try:

        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except Exception:
        return None
# 产生器
def parse_one_page(html):
    doc = pq(html)
    ul = doc('.bigimg')
    liList = ul('li')
    #print(type(liList),type(liList.items()))
    for li in liList.items():
        a = li('a:first-child')
        href = a[0].get('href')
        title = a[0].get('title')
        span = li('.search_now_price')
        price = span[0].text[1:]
        p = li('.search_book_author')
        author = p('a:first-child').attr('title')
        date = p('span:nth-child(2)').text()[1:]
        publisher = p('span:nth-child(3) > a').text()
        comment_number = li('.search_comment_num').text()[:-3]
        detail = li('.detail').text()
        yield {
            'href':href,
            'title':title,
            'price':price,
            'author':author,
            'date':date,
            'publisher':publisher,
            'comment_number':comment_number,
            'detail':detail
        }

if __name__ == '__main__':
    urls = ['http://search.dangdang.com/?key=python&act=input&sort_type=sort_default&page_index={}'.format(str(i)) for i in range(1,3)]
    infos = []
    for url in urls:
        book_infos = parse_one_page(get_one_page(url))
        content = list(book_infos)
        infos.extend(content)
    head = ['链接','书名','价格','作者','日期','出版社','评论数','详情']
    keys = ['href','title','price','author','date','publisher','comment_number','detail']
    write_to_xls(head,'dang.xls',infos,keys)



