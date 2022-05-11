"""
    思路: http://www.wwmulu.com/rj/nu/play-1-1.html
    1. 拿到主页面的页面源代码，找到iframe 
    2. 从iframe的页面源代码中拿到m3u8文件
    3. 下载第一次m3u8文件 -> 下载第二层m3u8文件(真实的视频地址)
    4. 下载视频
    5. 分析m3u8文件,视频文件需要下载秘钥，进行解密操作
    6. 合成ts文件为一个mp4文件
"""


import requests
from bs4 import BeautifulSoup
import asyncio
import aiofiles
import aiohttp
import re
from Cryptodome.Cipher import AES

def get_iframe_src_first_m3u8(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    main_page = BeautifulSoup(response.text, 'html.parser')
    src = main_page.find("iframe").get('src').split("u=")[1]
    return src
    # return "https://pps.sd-play.com/20220119/xL72qqGB/index.m3u8"


def download_m3u8_file(url, name, path):
    response = requests.get(url)
    with open(path+"m3u8/"+name, mode="wb") as f:
        f.write(response.content)


async def donwload_ts(ts_url, linename, path, session):
    async with session.get(ts_url) as response:
        async with aiofiles.open(path+linename, mode="wb") as f:
            await f.write( await response.content.read())
    print(f"{linename}下载完毕")


async def aio_download(name,path):
    tasks =[]
    # 优化代码不在下载ts download_ts中创建可以避免sessin多次创建
    async with aiohttp.ClientSession() as session: 
        async with aiofiles.open(path+"m3u8/"+name, mode="r", encoding="utf-8") as f:
            async for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                #line 是 .ts视频文件, 将文件url ，文件名传入下载内容中
                ts_url = line
                line = ts_url.split("/")[-1:][0]
                task = asyncio.create_task(donwload_ts(ts_url, line, path, session)) # 创建异步任务
                tasks.append(task)
            await asyncio.wait(tasks) # 等待任务结束


def get_key(url):
    response = requests.get(url)
    return response.text
    # return "6233b9bbd8ac9eba"

async def dec_ts(key, line, path): # 进行解密 加密方式为AES 
    aes = AES.new(key=key.encode('utf-8'), IV=b"0000000000000000", mode=AES.MODE_CBC)
    # 读 写
    async with aiofiles.open(path+line, mode="rb") as f1,\
        aiofiles.open(path+"temp_"+line, mode="wb") as f2:

        bs = await f1.read() # 读取原 ts文件
        await f2.write(aes.decrypt(bs)) #写入 解密后文件
    print(f"{line}处理完毕")

async def aio_dec(key, path, name):
    #解密 需要先读取ts文件让将文件解密再存入
    tasks = []
    async with aiofiles.open(path+'m3u8/'+name, mode="r") as f:
        async for line in f:
            line  = line.strip()
            if line.startswith("#"):
                continue
            # 开始创建异步任务 进行解密操作
            line = line.split("/")[-1:][0]
            task = asyncio.create_task(dec_ts(key, line, path))
            tasks.append(task)
        await asyncio.wait(tasks)

def merge_ts(path, name):
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    with open(path+"m3u8/"+name, mode="r", encoding="utf-8") as f,\
        open(path+'怒电影.mp4', mode="ab") as fw:
        for line in f:
            if line.startswith("#"):
                continue
            line = path + "temp_"+line.split("/")[-1:][0].strip() # 得到文件路径
            #循环路径将文件合并
            with open(line, mode="rb") as fwline:
                fw.write(fwline.read())
        print("视频合成完成")

def main(url, path):
    #1. 2. 拿到主页面的页面源代码，找到iframe，对应的url地址,获取到第一层的m3u8
    iframe_src_first_m3u8 = get_iframe_src_first_m3u8(url) # https://pps.sd-play.com/20220119/xL72qqGB/index.m3u8
    #3. 下载第一次m3u8文件 -> 下载第二层m3u8文件(真实的视频地址)
    download_m3u8_file(iframe_src_first_m3u8, "怒电影_first_m3u8.m3u8",path)
    #3.1 下载第二层m3u8文件 https://pps.sd-play.com/20220119/xL72qqGB/1200kb/hls/index.m3u8
    with open(path+"m3u8/怒电影_first_m3u8.m3u8", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            #拼接第二层m3u8的路径 /20220119/xL72qqGB/1200kb/hls/index.m3u8
            second_m3u8_url = iframe_src_first_m3u8.split("/20220119")[0] + line
            download_m3u8_file(second_m3u8_url, "怒电影_second_m3u8.m3u8", path )
            print("第二层m3u8下载完毕")
    
    #4. 下载视频 优化代码，使用异步协程加开下载------------------------------------
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aio_download("怒电影_second_m3u8.m3u8", path))
    # asyncio.run(aio_download("怒电影_second_m3u8.m3u8", path))

    #5.1 拿到秘钥 这里读出来的文件需要加一个read(),才能获取到内容
    with open(path+'m3u8/'+"怒电影_second_m3u8.m3u8", mode="r" ,encoding="utf-8") as fms:   
        key_url = re.search(r',URI="(?P<url>.*?)"', fms.read()).group("url")
    key = get_key(key_url)
    #5.2 进行解密 异步解密io操作
    loop.run_until_complete(aio_dec(key, path ,'怒电影_second_m3u8.m3u8'))
    # asyncio.run(aio_dec(key, path ,'怒电影_second_m3u8.m3u8'))

    #6. 合并所有的ts文件
    merge_ts(path, '怒电影_second_m3u8.m3u8')   



if __name__ == "__main__":
    path = "G:/python/async协程/video2/"
    url = "http://www.wwmulu.com/rj/nu/play-1-1.html"
    main(url,path)