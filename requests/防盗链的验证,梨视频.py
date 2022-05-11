import requests
# https://www.pearvideo.com/video_1749838
# https://video.pearvideo.com/mp4/short/20220425/1651573562049-15868345-hd.mp4
# https://video.pearvideo.com/mp4/short/20220425/cont-1749838-15868345-hd.mp4
# 1. 拿到contId 
# 2. 拿到vidoeStatus返回的json => srcUrl
# 3. srcUrl里面的内容进行修整
# 4. 下载视频

url = "https://www.pearvideo.com/video_1749838"
cont_id = url.split('_')[1]
videoStatusUrl = f"https://www.pearvideo.com/videoStatus.jsp?contId={cont_id}&mrd=0.349411448251693"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Referer": url 
}

res = requests.get(url=videoStatusUrl,headers=headers)
dic = res.json()

#组装视频地址
srcUrl = dic['videoInfo']['videos']['srcUrl']
systemTime = dic['systemTime']
srcUrl = srcUrl.replace(systemTime,f"cont-{cont_id}")

#下载视频
with open('G:/python/requests/video/a.mp4',mode='wb') as f:
    f.write(requests.get(url=srcUrl).content)
