import scrapy


class CityspiderSpider(scrapy.Spider):
    name = 'cityspider'
    allowed_domains = ['deyang.58.com']
    start_urls = ['https://deyang.58.com/?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT']

    def parse(self, response):
        content = response.body #二进制数据
        text = response.text #字符串
        xpath = response.xpath('//*[@id="bigLogo"]')[0] # 可以使用xpath语法
        css = response.css("#su::attr('value')") # 通过css 的方式获取数据
        print(xpath.extract_first()) # 获取selectr列表的第一条，
        print(xpath.extract) # 获取selectr对象的data [<Selector xpath='//*[@id="bigLogo"]' data='<img id="bigLogo" src="//img.58cdn.co...'>]
        pass
