
# <video src="不能播的视频.mp4"></video> 这样会到时视频加载过慢
# 一般的视频网站是怎么做的?
# 用户上传 -> 转码(把视频做处理, 2K, 1080, 标清)  -> 切片处理(把单个的文件进行拆分)  60
# 用户在进行拉动进度条的时候
# =================================

# 需要一个文件记录: 1.视频播放顺序, 2.视频存放的路径.
# M3U8  txt  json   => 文本

# 想要抓取一个视频:
#  1. 找到m3u8 (各种手段)
#  2. 通过m3u8下载到ts文件
#  3. 可以通过各种手段(不仅是编程手段) 把ts文件合并为一个mp4文件

""" 
    流程：
        1. 拿到https://cokemv.me/vodplay/39847-1-1.html 页面的源码
        2. 从源码中提取到m3u8的url
        3. 下载m3u8文件，检查文件是否加密等
        4. 合成视频
"""
# https://cokemv.org/webm3u8/bcde8b04514d1ca69091a87266891bee/1cb2e17ba820f37b79041e788df5ebf7/1652148765?name=1.m3u8
from operator import mod
from urllib import response
import requests
import re
import os


# 获取页面源码
def get_page_html(url):
    response = requests.get(url,headers)
    response.encoding = "utf-8"
    regex = re.compile(r'"link_pre":"","url":"(?P<m3u8>.*?)"')
    m3u8url= regex.search(response.text).group('m3u8').replace("\/",'/')
    domain = m3u8url.split("/webm3u8")[0]

    return {"m3u8url":m3u8url, "domain":domain}

# 获取m3u8 文件并保存
def get_m3u8(url): #https://cokemv.org/webm3u8/725d4cec15a4d0c265f6e14da08640a0/77dae31f888c294a4fb2aa81b7d879d0/1652153375?name=1.m3u8
    response = requests.get(url,headers)
    with open('G:/python/async协程/video/m3u8/妖神记.m3u8', mode="wb") as f:
        f.write(response.content)

# 下载视频片段 并通过 open 方法直接合并文件
def download_video_ts(domain):
    with open('G:/python/async协程/video/m3u8/妖神记.m3u8', mode="r") as f:
        for line in f:
            line = line.strip()  # 先去掉空格, 空白, 换行符
            if line.startswith("#"):
                continue
            #下载视频 合并 视频
            response = requests.get(f"{domain}{line}")

            # 方法一 
            with open("G:/python/async协程/video/妖神记.mp4", mode="ab") as fw:
                fw.write(response.content)
            print(line[-10:], '下载完成')

    # 将视频合并
    # print(os.popen(r"copy /b video/*.ts 01.mp4").read())
    # pass
def merge_src():
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    list = []
    with open('G:/python/async协程/video/m3u8/妖神记.m3u8', mode="r") as f:
        for line in f:
            line = line.strip()  # 先去掉空格, 空白, 换行符
            if line.startswith("#"):
                continue
            line = line[-10:]   
    os.system("copy /b /async协程/video/*.ts 01.mp4")

def main(url):
    # 1. 获取页面源码
    # dic_m3u8url_domain = get_page_html(url)
    # 2. 获取m3u8 文件并保存, 
    #get_m3u8(dic_m3u8url_domain["m3u8url"])
    #3. 下载视频片段 并通过 open 方法直接合并文件
    #download_video_ts(dic_m3u8url_domain["domain"])
    #3.2. 合并视频 通过os 模块
    merge_src()


if __name__ == "__main__":
    url = "https://cokemv.me/vodplay/39847-1-1.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }
    main(url)