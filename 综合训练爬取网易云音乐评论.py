# 1. 找到未加密的参数 # window.asrsea(参数,xxxx,xxx)
# 2. 想办法吧参数进行加密(必须参考网易的逻辑)，params => encText，encSecKey => encSecKey
# 3. 请求到网易，拿到评论信息



# 4. 安装pycryptodomex 提供加密技术 pip install pycryptodomex window系统安装pycryptodomex ubuntu系统安装pycryptodome
import requests
from Cryptodome.Cipher import AES
from base64 import b64encode
import json



# 请求方式是Post
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "A_PL_0_7419976107",
    "threadId": "A_PL_0_7419976107"
}

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
# 服务于d的
d = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
e = '0CoJUm6Qyw8W8jud'
b = '010001'
i = "PzShmrC74zGfVhD4" # 固定随机数 ， 网易是随机的

def get_encSecKey(): # 输出固定的值encSecKey，由于i是固定的所以c() 函数输出的encSecKey 为固定的
    return "0fad5c42ca4138d540b8c1d81fb6c753824b90d4051000dad0578c0515ff10292ed648cdf38d4de824cf5fe48e67c61de9c9eec63c433e67d40cb0aa23013d8139adeb9c8b1eb446f2341ba7934f3e3f61c20a45c484d9a192a2824164de93542578b85511d9f9390630c37c5587e29e7566cb7529ad16b2a90783ce246c7dfd"

#加密data
def get_params(data): # 默认接收到的是字符串
    # 第一次加密
    first_enc = enc_params(data, e)
    # 第二次加密
    second_enc = enc_params(first_enc, i)
    return second_enc # 返回params

#转换data 为16的倍数
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad  # 是余一就差15个，所以就需要放15个第15位置第字符，如果是16个 也需要放16个
    return data

def enc_params(data,key): #加密过程 , 默认接收到的是字符串
    iv = '0102030405060708' # 偏移量
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC) # 创建加密器, key iv 必须是bty字节格式,encode('utf-8') 转换为bty 字节格式
    bs = aes.encrypt(data.encode()) # 加密 加密内容的长度必须是16的倍数

    return str(b64encode(bs), 'utf-8') # 转换成字符串返回


# 处理加密过程
""" !function() {
    function a(a) { # 返回随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1) # 循环16次
            e = Math.random() * b.length, #随机数
            e = Math.floor(e), #取整
            c += b.charAt(e); #取字符中某位
        return c
    }
    function b(a, b) { # a 要加密的内容 ，b 是秘钥
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) # 是数据
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d, # 偏移量
            mode: CryptoJS.mode.CBC #加密模式CBC
        });
        return f.toString()
    }
    function c(a, b, c) { # c 不参数随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16); # 随机16字符
        return h.encText = b(d, g), # 第一次加密
        h.encText = b(h.encText, i), # 第二次加密 i是秘钥
        h.encSecKey = c(i, e, f), #得到encSecKey，e 和 f 是固定的，如果此时将i固定，得到的key一定是固定值，因为在c中没有随机设定
        h
    }
    function e(a, b, d, e) { a: 数据data, b:buV6P(["流泪", "强"]) '010001', d:buV6P(Rg9X.md), e:buV6P(["爱心", "女孩", "惊恐", "大笑"])
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
}(); """

# resp = requests.post(url, data={ # 需要将字典转换为json
#     "params":get_params(json.dumps(data)),
#     "encSecKey":get_encSecKey()
# })
# print(resp.text)