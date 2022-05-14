import scrapy
from dytt.items import DyttItem

class DyttsSpider(scrapy.Spider):
    name = 'dytts'
    allowed_domains = ['m.dytt8.net']
    start_urls = ['https://m.dytt8.net/html/gndy/dyzz/index.html']

    def parse(self, response):
        html = response.xpath('//*[@id="header"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/ul//table')
        for table in html:
            name = table.xpath("./tr[2]/td[2]/b/a/text()").extract_first()
            src = table.xpath("./tr[2]/td[2]/b/a/@href").extract_first()
            
            url = "https://m.dytt8.net"+src
            #对第二个页面发起访问
            yield scrapy.Request(url=url, callback=self.parse_second, meta={'name':name})
            
    def parse_second(self, response):
        src = response.xpath('//div[@id="Zoom"]//img/@src').extract_first()
        # 接收meta 的参数
        name = response.meta['name']

        movie = DyttItem(src=src, name=name)
        yield movie