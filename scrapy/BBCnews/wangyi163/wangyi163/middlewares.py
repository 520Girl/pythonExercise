

from scrapy import signals
from scrapy.http import HtmlResponse
from time import sleep


class Wangyi163SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Wangyi163DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    #! 2.1 拦截新闻主体的响应对象，因为这里是异步数据， spider 为全局对象
    def process_response(self, request, response, spider):
        #lamb 选择指定的链接进行拦截， 通过request.url 和spider.model_urls中的链接进行对比
        #? 如果存在就异步加载数据返回xpath对象，如果不存在就将原对象返回
        if request.url in spider.model_urls:
            bro = spider.bro #* 获取爬虫类中定义的浏览器对象
            bro.get(request.url) #* 对五大板块对象进行请求
            sleep(3)
            page_text = bro.page_source #* 包含了动态加载的新闻数据
            new_response = HtmlResponse(url=request.url,body=page_text,encoding="utf-8",request=request)
            return new_response
        else:
            return response

    def process_request(self, request, spider): 
        return None

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
