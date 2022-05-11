import requests
import json

url = "https://passport.17k.com/ck/user/login"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
data={
    "loginName": "发发发法法",
    "password": "大法法"
}

#创建一个session
session = requests.session()
res = session.post(url,data=data)
# print(res.json())

# 通过session 这个借口获取到cookie 请求收藏数据
res = session.get("收藏接口")
print(res.json())