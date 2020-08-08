#header = ['name','age']
#content= [{'a':2,'b':3},{'a':4,'b':5}]
#keys = ['a','b']
def write_to_xls(header,sheet_name,content,keys):
    import xlwt
    import time
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet(sheet_name)
    for i in range(len(header)):
        sheet.write(0, i, header[i])
    for row in range(1,len(content)+1):
        time.sleep(1)
        for col in range(len(keys)):
            sheet.write(row,col,content[row-1][keys[col]])
    print('已写入Excel')
    book.save(sheet_name)

def getheader(file):
    import re
    headerDict={}
    with open(file,'r') as f:
        headerContent = f.read()
        headers=re.split('\n',headerContent)
        for item in headers:
            res = re.split(':',item,maxsplit=1)
            headerDict[res[0]]=res[1].lstrip()
    return headerDict

def webDriver_wait(elements_name,browser,flag):
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    try:
        wait = WebDriverWait(browser, 60)
        if flag=='1':
            wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, elements_name)))
        if flag=='2':
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, elements_name)))
        return True
    except:
        return False