import requests
import json
import random
import string
import os

word = input("请输入搜索关键字：")
print(word)
dir_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
print('图像文件将保存在',dir_name,'目录中')
os.mkdir(dir_name)
max_value = 100
current_value = 0
image_index = 1
while current_value < max_value:
    result = requests.get('https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%9D%8E%E5%AE%81&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=girl&pn={}&rn=30&gsm=1e&1552906917704='.format(word,current_value))

    json_str = result.content
    json_doc = str(json_str, 'utf-8')
    imageResult = json.loads(json_doc)
    data = imageResult['data']
    for record in data:
        url = record.get('middleURL')
        if url != None:
            print('正在下载图片：',url)
            r = requests.get(url)
            filename = dir_name + '/' + str(image_index).zfill(10) + ".png"
            with open(filename, 'wb') as f:
                f.write(r.content)
            image_index += 1

    current_value += 30
print('图像下载完成')

