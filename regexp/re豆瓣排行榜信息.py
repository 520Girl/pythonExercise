import requests
import re
import csv

url = "https://movie.douban.com/chart"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
res = requests.get(url,headers=headers)
res.encoding = 'utf-8'
page_content = res.text

regexp = re.compile(r'<table width="100%" class="">.*?<td width="100" valign="top">.*?'
                    r'<a class="nbg" href=".*?"  title="(?P<title>.*?)">.*?<div class="pl2">.*?'
                    r'<div class="star clearfix">.*?<span class="rating_nums">(?P<score>.*?)</span>.*?<span class="pl">(?P<scorePeople>.*?)</span>',re.S)
#开始匹配
result = regexp.finditer(page_content)
#写入文件
f = open('G:/python/regexp/data.csv',mode='w',encoding='utf-8')
csvwrite = csv.writer(f)
for item in result:
    # 将item group转换为dict 字典
    dic = item.groupdict()
    dic['scorePeople'] = dic['scorePeople'].replace('(','').replace(')','')
    dic['title'] = dic['title'].strip()
    # print(item.group('score'))
    # print(item.group('title').strip())
    # print(item.group('scorePeople').replace('(','').replace(')',''))
    csvwrite.writerow(dic.values())

f.close()