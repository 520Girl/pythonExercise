# 1. 拿到页面源码
# 2. 使用bs4进行解析， 拿到数据

import requests
from  bs4 import BeautifulSoup
import csv

url = "http://xinfadi.com.cn/priceDetail.html"
resp = requests.get(url)
print(resp.text)

#将查询到的数据存入文件中
f = open("G:/python/菜价.csv")
csvwriter = csv.writer(f)

#解析数据
# 1. 把页面源代码交给beautifulSoup进行处理，生成bs对象
page = BeautifulSoup(resp.text, "html.parser") #指定html 解析器
# 2. 从bs对象中查询数据
#find(标签 属性=值)
# find_all(标签, 属性=值)
# table = page.find("table", class_="hq_table") # class是python的关键字

table = page.find("table", attrs={"class":"hq_table"}) # 和上一行是一个意思，此时可以避免clas
# 拿到所有数据行,第一行除外
trs = table.find_all("tr")[1:] 
for tr in trs: #获取到每一行
    tds = tr.find_all("td") #拿到每行中的所有td
    name = tds[0].text 
    low = tds[1].text
    avg = tds[2].text
    hight = tds[3].text
    gui = tds[4].text
    kind = tds[5].text
    date = tds[6].text
    csvwriter.writerow([name,low,avg,hight,gui,kind,date])

