import scrapy
from dangdang.items import DangdangItem

class DangSpider(scrapy.Spider):
    name = 'dang'
    allowed_domains = ['bang.dangdang.com']
    start_urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1']

    base_url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-"
    page = 1

    def parse(self, response):
        # 1. 管道pipelines下载数据
        # 2. 定义数据结构item
        html = response.xpath("/html/body//ul[@class='bang_list clearfix bang_list_mode']/li")
        for li in html:
            src = li.xpath(".//div/a/img/@src").extract_first()
            name = li.xpath(".//div/a/img/@alt").extract_first()
            price = li.xpath(".//div[@class='price']/p/span[1]/text()").extract_first()
            #提交给管道下载数据
            book = DangdangItem(src=src, name=name, price=price, page=self.page)
            yield book #生成器generator ,用来迭代，获取一个book 就交给一个pipeline管道

        #爬取多页数据
        if self.page < 25:
            self.page  = self.page + 1
            url = self.base_url  + str(self.page)
            # 调用parse 方法
            # scrapy.Request 为scrapy的get方法，url 就是请求的地址，callback是需要执行的函数，
            # 注意这里的allowed_domains 必须不是详细地址应该为domain地址这样就不会阻止爬虫了
            yield scrapy.Request(url=url, callback=self.parse)
