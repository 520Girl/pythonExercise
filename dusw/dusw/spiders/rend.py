import imp
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dusw.items import DuswItem


class RendSpider(CrawlSpider):
    name = 'rend'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1617_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/book/1617_\d+\.html'),  # 匹配的地址信息
            callback='parse_item',
            follow=False), # false关闭多页面爬虫
    )

    def parse_item(self, response):
        img_url = response.xpath("//div[@class='bookslist']//img")

        for img in img_url:
            name = img.xpath("./@alt").extract_first()
            src = img.xpath("./@data-original").extract_first()
            book = DuswItem(name=name, src=src)    
            yield book
