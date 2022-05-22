import scrapy
# 代理ip的使用

class AgentSpider(scrapy.Spider):
    name = 'agent'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/s?wd=ip']

    def parse(self, response):
        page_text = response.text
        with open('ip.html', "w", encoding="utf-8") as fp:
            fp.write(page_text)
