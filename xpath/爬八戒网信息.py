from re import S
from lxml import etree
import requests
import time
import csv

#因为八戒网改为借口类型，现在改爬包子漫画
url = "https://cn.webmota.com/"
resp = requests.get(url)
resp.encoding ="utf-8"

#写入文件
f = open('G:/python/xpath/data.csv',mode="w",encoding="utf-8")
csvwrite = csv.writer(f)

#通过lxml 解析html
html = etree.HTML(resp.text)
divs = html.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div')
for item in divs:
    name = item.xpath('normalize-space(./a/@title)') # 漫画title,去掉空格
    rank = item.xpath('./div[@class="comics-card__badge"]/text()') #排名 有些没有排名所以不能直接通过下标获取
    rank = rank[0] if len(rank) > 0 else '' 
    #对数据进行处理去掉空格 使用生成器
    type = item.xpath('./a[1]/div/span/text()') #类型
    type = list(( item.strip() for item in type))
    if len(type) > 1 :
        type =  f"{type[0]}|{type[1]}"
    else:
        type = type[0]
    note = item.xpath('./a[2]/small[@class="tags"]/text()')[0].strip() #提示
    hrefUrl = item.xpath('./a[1]/amp-img/@src')[0].strip()
    
    # 写入文件
    csvwrite.writerow([name, rank, type, note, hrefUrl])
print("写入完成！")