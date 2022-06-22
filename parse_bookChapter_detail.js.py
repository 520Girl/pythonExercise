

import os
from unittest import result
import requests
import re
import json
url = 'http://www.sixmh7.com/16041/1377459.html'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
reponse = requests.get(url)
reponse.encoding = "utf-8"

regex = re.compile(r".*?eval(?P<javaScript>.*?)</script>",re.S)
re_list = regex.search(reponse.text)

# 添加括号变成自执行函数
javaScript = re_list.group('javaScript')
javaScript = javaScript.replace("('g",")('g").replace("}))","})")
# 添加console.log 输出结果
javaScript = f'console.log({javaScript})'
print(javaScript)
# print(reponse.text)  #以字符串形式打印网页源码
with open("G:/python/index2.js", mode="w") as f:
    f.write(javaScript)

cmd = 'node -e "require(\\"%s\\")"' % ('./index.js')
print(cmd)
pipeline = os.popen(cmd)
# 读取结果
result = pipeline.read()
print('结果是:',result.strip())

# 将结果进行处理
result = 'var newImgs=["https://p3.byteimg.com/tos-cn-i-8gu37r9deh/092b7dd1e0bb41c9bb37fc2cd5d1770a~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/6acc9f3e6f6342e58c265007b2dd7717~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/cf6296c57d1d47b9b209e3ec190f7a7f~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/4417f79a614f4bf2993c1ef36ae7f6cc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/bc6c32f704074086a40c106f9637c8b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d5ec578ec93f4154b4aa388572e6d57d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/54a904b9232b45bbbb794324d58e3f33~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/f8feea0ea88041a38353b024de4c54f9~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/2c5cc398c71c490f9c86df4a76b9ebdc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/63a1a67347034915bc9d20643118932d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d9014265b0464a569ff0840f868942b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/7fefdd62d7744e16b888ac6e1e38dba3~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/80a4dd2a34e04a71a6ac714cc5c2f97f~noop.jpg"]'
regex3 = re.compile(r"var newImgs=(?P<javaScripts>.*?)$", re.S)
data = regex3.search(result)
print(data.group('javaScripts'))
print(len(json.loads(data.group('javaScripts'))))




# console.log((function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p})('g e=["2://1.5.0/4-7-i-8/d~6.3","2://1.5.0/4-7-i-8/c~6.3","2://1.5.0/4-7-i-8/b~6.3","2://1.5.0/4-7-i-8/a~6.3","2://1.5.0/4-7-i-8/9~6.3","2://1
# .5.0/4-7-i-8/f~6.3","2://1.5.0/4-7-i-8/l~6.3","2://1.5.0/4-7-i-8/o~6.3","2://1.5.0/4-7-i-8/n~6.3","2://1.5.0/4-7-i-8/m~6.3","2://1.5.0/4-7-i-8/h~6.3","2://1.5.0/4-7-i-8/j~6.3","2://1.5.0/4-7-i-8/k~6.3"]',25,25,'com|p3|https|jpg|tos|byteimg|noop|cn|8gu37r9deh|bc6c32f704074086a40c106f9637c8b1|4417f79a614f4bf2993c1ef36ae7f6cc|cf6296c57d1d47b9b209e3ec190f7a7f|6acc9f3e6f6342e58c265007b2dd7717|092b7dd1e0bb41c9bb37fc2cd5d1770a|newImgs|d5ec578ec93f4154b4aa388572e6d57d|var|d9014265b0464a569ff0840f868942b1||7fefdd62d7744e16b888ac6e1e38dba3|80a4dd2a34e04a71a6ac714cc5c2f97f|54a904b9232b45bbbb794324d58e3f33|63a1a67347034915bc9d20643118932d|2c5cc398c71c490f9c86df4a76b9ebdc|f8feea0ea88041a38353b024de4c54f9'.split('|'),0,{})
# )
# 结果是: var newImgs=["https://p3.byteimg.com/tos-cn-i-8gu37r9deh/092b7dd1e0bb41c9bb37fc2cd5d1770a~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/6acc9f3e6f6342e58c265007b2dd7717~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/cf6296c57d1d47b9b209e3ec190f7a7f~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/4417f79a614f4bf2993c1ef36ae7f6cc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/bc6c32f704074086a40c106f9637c8b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d5ec578ec93f4154b4aa388572e6d57d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/54a904b9232b45bbbb794324d58e3f33~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/f8feea0ea88041a38353b024de4c54f9~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/2c5cc398c71c490f9c86df4a76b9ebdc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/63a1a67347034915bc9d20643118932d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d9014265b0464a569ff0840f868942b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/7fefdd62d7744e16b888ac6e1e38dba3~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/80a4dd2a34e04a71a6ac714cc5c2f97f~noop.jpg"]



# import execjs
# import os

# execjs.get().name # this value is depends on your environment.
# os.environ["EXECJS_RUNTIME"] = "Node"
# ctx = execjs.eval("""(function(p, a, c, k, e, d) {
# 	e = function(c) {
# 		return c.toString(36)
# 	};
# 	if (!''.replace(/^/, String)) {
# 		while (c--) {
# 			d[c.toString(a)] = k[c] || c.toString(a)
# 		}
# 		k = [function(e) {
# 			return d[e]
# 		}];
# 		e = function() {
# 			return '\\w+'
# 		};
# 		c = 1
# 	};
# 	while (c--) {
# 		if (k[c]) {
# 			p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c])
# 		}
# 	}
# 	return p
# })('g e=["2://1.5.0/4-7-i-8/d~6.3","2://1.5.0/4-7-i-8/c~6.3","2://1.5.0/4-7-i-8/b~6.3","2://1.5.0/4-7-i-8/a~6.3","2://1.5.0/4-7-i-8/9~6.3","2://1.5.0/4-7-i-8/f~6.3","2://1.5.0/4-7-i-8/l~6.3","2://1.5.0/4-7-i-8/o~6.3","2://1.5.0/4-7-i-8/n~6.3","2://1.5.0/4-7-i-8/m~6.3","2://1.5.0/4-7-i-8/h~6.3","2://1.5.0/4-7-i-8/j~6.3","2://1.5.0/4-7-i-8/k~6.3"]', 25, 25, 'com|p3|https|jpg|tos|byteimg|noop|cn|8gu37r9deh|bc6c32f704074086a40c106f9637c8b1|4417f79a614f4bf2993c1ef36ae7f6cc|cf6296c57d1d47b9b209e3ec190f7a7f|6acc9f3e6f6342e58c265007b2dd7717|092b7dd1e0bb41c9bb37fc2cd5d1770a|newImgs|d5ec578ec93f4154b4aa388572e6d57d|var|d9014265b0464a569ff0840f868942b1||7fefdd62d7744e16b888ac6e1e38dba3|80a4dd2a34e04a71a6ac714cc5c2f97f|54a904b9232b45bbbb794324d58e3f33|63a1a67347034915bc9d20643118932d|2c5cc398c71c490f9c86df4a76b9ebdc|f8feea0ea88041a38353b024de4c54f9'.split('|'), 0, {})""")
# print(ctx)



# import execjs
# import os

# execjs.get().name # this value is depends on your environment.
# os.environ["EXECJS_RUNTIME"] = "Node"
# ctx = execjs.compile("""function name(p, a, c, k, e, d) {
# 	e = function(c) {
# 		return c.toString(36)
# 	};
# 	if (!''.replace(/^/, String)) {
# 		while (c--) {
# 			d[c.toString(a)] = k[c] || c.toString(a)
# 		}
# 		k = [function(e) {
# 			return d[e]
# 		}];
# 		e = function() {
# 			return '\\w+'
# 		};
# 		c = 1
# 	};
# 	while (c--) {
# 		if (k[c]) {
# 			p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c])
# 		}
# 	}
# 	return p
# }""")
# print(ctx.call())

