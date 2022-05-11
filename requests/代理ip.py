import requests

# 140.250.152.1:8888 

url = "https://www.baidu.com/"

proxies = {
    "http":"http://140.250.152.1:8888"
}

res = requests.get(url,proxies=proxies)
res.encoding = 'utf-8'
print(res.text)