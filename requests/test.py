from base64 import encode
import requests

url = "https://www.baidu.com/"
reponse = requests.get(url)
reponse.encoding = "utf-8"
print(reponse.text)  #以字符串形式打印网页源码