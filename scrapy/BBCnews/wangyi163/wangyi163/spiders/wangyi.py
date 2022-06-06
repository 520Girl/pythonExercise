from ast import Try
from ntpath import join
import scrapy
import time
from selenium import webdriver
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from wangyi163.items import Wangyi163Item # 导入数据结构
import unicodedata # 去除uncode 的空白字符
import re # 将字符转中的通过unicodedata转义的空格替换为$nbsp;
import json # 将字符串转为python字典



# 增量式爬虫 也就是爬取的时候和数据库进行对比，数据库是否存在
# 1. https://news.163.com/根据导航到获取到指定的标签新闻 ，国内 国外....
# 2. 访问国内国外新闻主体，获取到今日推荐热点新闻标题，该页面是异步数据需要使用selenium 进行异步数据加载
# 3. 获取到新闻内容  

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.163.com']
    start_urls = ['https://news.163.com/']
    #lamb 用于报错获取到的新闻主体的链接设置全局变量
    model_urls = []

    #! 初始化项目 创建selenium需要的容器, 连接数据库，方便增量式爬虫
    def __init__(self):
        #lamb 1. 创建selenium 容器
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #路径改成自己的
        chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
        self.bro = webdriver.Chrome(chrome_options=chrome_options)

        #lamb 2. 连接数据库
        #? 2.1 配置文件读取 数据库配置信息
        setting = get_project_settings()
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.password = setting['DB_PASSWORD']
        self.host = setting['DB_HOST']

        #? 2.2 连接数据库
        myclient = MongoClient(f"mongodb://{self.user}:{int(self.password)}@{self.host}:{int(self.port)}/navigation")
        mydb = myclient.navigation
        self.mycol = mydb['news']
        # c = self.mycol.find_one({"title":"巴西KC-390战术运输机上的厕所ws"})
        # print(c)
        # for i in c:
        #     print(1)
        #     print(i)
        
    #! 1. 获取国内国外新闻主体链接
    def parse(self, response):
        li_list = response.xpath('//div[@class="index_head"]/div[@class="bd"]/div[@class="ns_area list"]/ul/li')
        # alist = [2,3,5,6] # 国内 国际 航空 军事
        alist = [2,3,5,6] # 国内 国际 航空 军事
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first() # 获取页面url
            model_url_text = li_list[index].xpath('./a/text()').extract_first()
            self.model_urls.append({"url":model_url,"text":model_url_text})
        
        #lamb 一次对每个新闻主体的链接进行请求
        for url in self.model_urls:
            yield scrapy.Request(url=url['url'], callback=self.parse_model,meta={"text":url['text']})
    
    #! 2. 访问新闻主体页面，获取到里面的热点新闻，这里的数据是异步加载的所以需要用到selenium
    def parse_model(self, response):
        today_news_text = response.xpath("//div[@class='today_news']/h2/text()").extract_first()
        today_news_li = response.xpath("//div[@class='today_news']/ul/li")
        
        #lamb 2.1 判断是否是 今日推荐，是则进行爬取，否则终止
        if today_news_text == "今日推荐":
            for li in today_news_li:
                title = li.xpath("./a/text()").extract_first()
                new_detail_url = li.xpath("./a/@href").extract_first()

                #? 将数据提交给数据结构item ,后面请求接口代替
                # item = Wangyi163Item()
                # item['title'] = title
                #lamb 2.2 和数据库数据进行对比 增量爬虫，看数据是否存在
                dbTitle = self.mycol.find_one({"title":title}) 
                dbnewsHref = self.mycol.find_one({"newsHref":new_detail_url})
                if dbTitle != None or dbnewsHref != None:
                    continue
    
                #* 将新闻详情页的链接提交个新方法进行处理
                yield scrapy.Request(url=new_detail_url, callback=self.parse_model_detail, meta={"url":new_detail_url,"text":response.meta['text']})
                

    #! 3. 新闻详情页信息进行解析分析
    def parse_model_detail(self, response):
        print(response.meta['url'])
        #lamb 判断是文章样式article[https://www.163.com/dy/article/H95QQF1I0514R9OJ.html]
        #lamb 还是轮播图样式photoview[https://war.163.com/photoview/4T8E0001/2313698.html#p=H95T3T9S4T8E0001NOS], 
        url = response.meta['url']
        response.meta['newsHref'] = url
        if 'article' in url:
            response.meta['type'] = 'article'
            return self.model_detail_article(response)
        else:
            response.meta['type'] = 'photoview'
            return self.model_detail_slider(response)

    #! 3.1 新闻详情页样式一 文章样式
    def model_detail_article(self,response):
        #lamb content 内容，带有换行符,
        content = response.xpath('//*[@class="post_body"]').extract()
        content = unicodedata.normalize('NFKC', content[0])    # 去除文本中的空格
    
        #lamb 1. title,判断和 新闻主体那个长，选择短的做新闻标题， 后面请求 接口代替
        title = response.xpath('//h1[@class="post_title"]/text()').extract_first()
        commentNum = 0
        # if len(title) < len(response.meta['item']['title']):
        #     title = response.meta['item']['title']
        
        #lamb 2. createTime创建爬虫的时间
        createTime = time.time()

        #lamb 4. rbelong 新闻本身属于哪个新闻，cbelong新闻爬取的是哪个的新闻, cauthor新闻发布者,time 新闻本身发布时间,address 发文地,最后一项为归类
        time_address = response.xpath('//*[@class="post_info"]/text()').extract_first().split("来源: ")
        dic_time = time_address[0].strip()
        address = [time_address[1].strip(),response.meta['text']]
        timeArray = time.strptime(dic_time, "%Y-%m-%d %H:%M:%S") #转换成时间数组
        dic_time = time.mktime(timeArray) #转换成时间戳
        rbelong =  response.xpath('//*[@class="post_info"]/a[1]/text()').extract_first().strip()
        cbelong = "网易新闻"
        cauthor_num = -1 if content.rfind("。(编译/") == -1 else content.rfind("。(编译/")
        if cauthor_num == -1:
            cauthor = ''
        else:
            cauthor_p = content.rfind(')</')
            cauthor = content[cauthor_num+2:cauthor_p]

        #lamb 7. rimg 原本文章中的新闻， type 文章类型 
        release_img = re.compile(r'<p class="f_center">.*?<img src="(?P<imgUrl>.*?)">.*?</p>', re.S) # 使用re模块匹配imgUrl
        release_img = release_img.finditer(content)
        rimg = [] # 原始的imgUrl
        # print(rimg.group())
        # print(re.sub(r'/<[a-zA-Z]+.*?>([\s\S].*?)<\/[a-zA-Z]*?>/g','&nbsp;', content))
        for img in release_img: # 将匹配的链接放入rimg
            rimg.append({"url":img.group('imgUrl'),"alt":""})
        type = response.meta['type']

        #lamb 9.sbelong 1热门，2最新，3要点, 
        sbelong = 1

        #lamb 11. newsHref 新闻源头链接, commentNum 评论人数, keyword 关键字
        newsHref = response.meta['newsHref']
        keyword = response.xpath("//meta[@name='keywords']/@content").extract_first().split(',')
        topList = -1
        weight = 1
        puTime = 0
        heartNum = 0
        eyeNum = 0

        #lamb 组装数据
        item= {
            "time":dic_time,
            "createTime":createTime,
            "rbelong":rbelong,
            "cbelong":cbelong,
            "cauthor":cauthor,
            "rimg":rimg,
            "type":type,
            "content":content,
            "sbelong":sbelong,
            "newsHref":newsHref,
            "topList":topList,
            "keyword":keyword,
            "weight":weight,
            "puTime":puTime,
            "heartNum":heartNum,
            "eyeNum":eyeNum,
            "title":title,
            "commentNum":commentNum,
            "address":address
        }

        # print(dic_time,createTime,rbelong,cbelong,cauthor,rimg,type,content,sbelong,newsHref,topList,keyword)

        #lamb 请求接口获取接口数据
        regex = re.compile(r'var config = {.*?"productKey": "(?P<productKey>.*?)",.*?"docId": "(?P<docId>.*?)",.*?};', re.S)
        # print(response.text)
        config = regex.search(response.text)
        productKey = config.group('productKey')
        docId = config.group('docId')
        url = f'https://comment.api.163.com/api/v1/products/{productKey}/threads/{docId}?ibc=jssdk'
        yield scrapy.Request(url,callback=self.detail_slider_comment,dont_filter=True, meta={"item":item})

    #! 3.2 新闻详情页样式二 轮播图样式
    def model_detail_slider(self, response):
     
        #lamb 1. title, commentNum判断和 新闻主体那个长，选择短的做新闻标题， 后面请求 接口覆盖
        title = response.xpath('//div[@class="headline"]/h1/text()').extract_first()
        commentNum = 0
        # if len(title) < len(response.meta['item']['title']):
        #     title = response.meta['item']['title']
        
        #lamb 2. createTime创建爬虫的时间
        createTime = time.time()

        #lamb 4. rbelong 新闻本身属于哪个新闻，cbelong新闻爬取的是哪个的新闻, cauthor新闻发布者,time 新闻本身发布时间,
        rbelong_xpath = response.xpath("//textarea[@name='gallery-data']/text()").extract_first()
        dct_detail = json.loads(rbelong_xpath)
        rbelong = dct_detail['info']['source']
        cbelong = "网易新闻"
        cauthor = dct_detail['info']['dutyeditor']
        dic_time = dct_detail['info']['lmodify'] # 将实际字符转为时间戳
        timeArray = time.strptime(dic_time, "%Y-%m-%d %H:%M:%S") #转换成时间数组
        dic_time = time.mktime(timeArray) #转换成时间戳

        #lamb 7. rimg 原本文章中的新闻， type 文章类型 
        rimg = []
        for list in dct_detail['list']:
            rimg.append({"url":list['img'],"alt":list['note']})
        type = response.meta['type']

        #lamb 9. content 内容，带有换行符, sbelong 1热门，2最新，3要点, 
        content = ''
        sbelong = 1

        #lamb 11. newsHref 新闻源头链接, commentNum 评论人数, keyword 关键字
        newsHref = response.meta['newsHref']
        # commentNum = response.xpath("//div[@id='tieArea']//spam[@class='tie-info']/a[2]/text()").extract_first()
        keyword = response.xpath("//meta[@name='keywords']/@content").extract_first().split(',')
        topList = -1
        weight = 1
        puTime = 0
        heartNum = 0
        eyeNum = 0
        #lamb 组装数据
        item= {
            "time":dic_time,
            "createTime":createTime,
            "rbelong":rbelong,
            "cbelong":cbelong,
            "cauthor":cauthor,
            "rimg":rimg,
            "type":type,
            "content":content,
            "sbelong":sbelong,
            "newsHref":newsHref,
            "topList":topList,
            "keyword":keyword,
            "weight":weight,
            "puTime":puTime,
            "heartNum":heartNum,
            "eyeNum":eyeNum,
            "title":title,
            "commentNum":commentNum,
            "address":[response.meta['text']]
        }

        #lamb 请求接口获取接口数据
        regex = re.compile(r'var config = {.*?"productKey" : "(?P<productKey>.*?)",.*?"docId" : "(?P<docId>.*?)",.*?}', re.S)
        config = regex.search(response.text)
        productKey = config.group('productKey')
        docId = config.group('docId')
        url = f'https://comment.api.163.com/api/v1/products/{productKey}/threads/{docId}?ibc=jssdk'
        yield scrapy.Request(url,callback=self.detail_slider_comment,dont_filter=True, meta={"item":item})

        # print(title,dic_time,createTime,rbelong,cbelong,cauthor,rimg,type,content,sbelong,newsHref,commentNum,topList,keyword)

    def detail_slider_comment(self, response):
        res_json = json.loads(response.text)
        item = {}
        if response.status == 200:
            try: #请求接口
                commentNum = res_json['cmtCount']
                title = res_json['title']

                #将数据交个管道 存储数据库

                # item = Wangyi163Item()
                item['title'] = title
                item['commentNum'] = commentNum
            except Exception as err:
                pass
        
        item['state'] = 1
        item = {**response.meta['item'],**item} # 字典谁在后面覆盖前面的相同字段
        yield item
        
        
