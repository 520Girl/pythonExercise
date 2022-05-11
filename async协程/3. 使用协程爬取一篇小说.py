# 1 . 通过章节目录：https://www.soshuw.com/WuLianDianFeng/ 获取章节信息
# 2. 通过章节目录获取到的信息访问小说详细内容 https://www.soshuw.com/WuLianDianFeng/319110.html


import requests
import asyncio
import aiohttp
import aiofiles
from lxml import etree
from tqdm import tqdm
headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}

#异步下载小说
async def aiodownload(title,url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url,headers=headers) as response:
            response.encoding = "utf-8"
            content = getContent( await response.text())
            async with aiofiles.open("G:/python/async协程/files/"+title+'.txt', mode="w", encoding="utf-8") as f:
                await f.write(content) # 把小说内容写入
            
# 解析小说详情页面的内容
def getContent(text):
    # print(text)
    html = etree.HTML(text)
    content = html.xpath('/html/body//div[@class="content"]/text()')
    # 使用生成器 遍历去掉 \xa0\xa0\xa0\xa0 空格等
    content = list((item.replace(" ",'').replace("\xa0\xa0\xa0\xa0",'') for item in content))
    return ''.join(content)

#同步任务获取章节信息 
async def getCatalog(url): 
    response = requests.get(url)
    response.encoding = "utf-8"
    #通过lxml 解析html
    html = etree.HTML(response.text)
    dds = html.xpath('/html/body//div[@class="quanwen"]/div[@id="novel575"]/dl[1]/dd')
    tasks = []
    for item in tqdm(dds):
        title = item.xpath("./a/text()")[0]
        url = f'https://www.soshuw.com{item.xpath("./a/@href")[0]}'
        #print(title,url)
        # 执行异步任务下载小说页面
        if url != "https://www.soshuw.com/WuLianDianFeng/319186.html":
            tasks.append(asyncio.create_task(aiodownload(title,url)))
    await asyncio.wait(tasks)        
    


if __name__ == "__main__":
    url = "https://www.soshuw.com/WuLianDianFeng/"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getCatalog(url))
    # asyncio.run(getCatalog(url))
