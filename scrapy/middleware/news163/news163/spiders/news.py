# 需求，爬取网易新闻中的新闻数据
# 1. 通过网易新闻的首页解析出五大板块对应的消息的详情页的url（这里不是动态数据）
# 2. 每个板块对应的新闻标题都是动态加载进来的（动态加载进来的，这里不是请求的ajax数据，应该就是用到了懒加载）
# 3. 通过解析出来每一条详情页的url获取详细页的页面源码，解析出新闻的内容 

import scrapy
from selenium import webdriver
from news163.items import News163Item


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['news.163.com','www.163.com']
    start_urls = ['http://news.163.com/']
    #存储详情页的url
    model_urls = []

    #!实例化浏览器使用selenium
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #路径改成自己的
        chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
        self.bro = webdriver.Chrome(chrome_options=chrome_options)

        # self.bro = webdriver.Chrome(executable_path="F:\IDM\chromedriver_win32\chromedriver.exe")

    def parse(self, response):
        li_list = response.xpath('//div[@class="index_head"]/div[@class="bd"]/div[@class="ns_area list"]/ul/li')
        #获取的列表项 的详情页面url
        # alist = [2,3,5,6]
        alist = [2,3,5] # 国内 国际 航空 军事
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first() # 获取页面url
            self.model_urls.append(model_url)
        
        # print(self.model_urls)
        #依次对每一个板块对应的页面进行请求
        for url in self.model_urls:
            yield scrapy.Request(url, callback=self.parse_model)
    
    #!这里是异步数据 第二部,在中间中处理返回
    def parse_model(self,response): #解析每一个板块页面中对应的新闻的标题和新闻详情页的url
        div_list = response.xpath("//div[@class='ndi_main']/div")
        for div in div_list:
            # print(len(div_list[]))
            title = div.xpath('.//div[@class="news_title"]/h3/a/text()').extract_first()
            # img = div.xpath('./a[@class="ns_pic"]/img/@src').extract_first() or ''
            new_detail_url = div.xpath('.//div[@class="news_title"]/h3/a/@href').extract_first() # 详情页的链接
            
            #回调需要保持的数据
            item = News163Item()
            item['title'] = title

            #请求详情页 第三部分
            yield scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item':item})

    def parse_detail(self,response):
        content = response.xpath('//*[@class="post_body"]/p/text()').extract()
        content = ''.join(content)

        item = response.meta['item']
        item['content'] = content
        #提交给管道
        yield item

# 关闭浏览器
    def closed(self,spider):
        self.bro.quit()