
# 爬取的网址是 http://www.sixmh7.com/ 6漫画，先爬取几个常看的漫画的全部章节
#1. 使用增量爬虫的crawlSpider的爬虫
#2. 先爬取漫画的详细信息， 通过信息爬取漫画的章节信息， 通过章节信息爬取的内容
import scrapy
import time
import json
import re
import os

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nav.items import NavItem


class A6cartoonSpider(CrawlSpider):
    name = '6cartoon'
    allowed_domains = ['sixmh7.com']
    start_urls = ['http://www.sixmh7.com/rank/1-1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/rank/1-\d+\.html'), callback='parse_item', follow=True),
    )

    #! 获取到 页面排行榜数据
    def parse_item(self, response):
        cy_list_mh = response.xpath('//div[@class="cy_list_mh"]/ul')

        item = NavItem()
        for list in cy_list_mh:
            # title
            title = list.xpath('./li[@class="title"]/a/text()').extract_first()
            item['title'] = title
            # 状态
            sbelong = list.xpath('./li[@class="zuozhe"]/text()').extract_first().split("：")[1]
            if sbelong == '连载中':
                item['sbelong'] = 1
            elif sbelong == '完结':
                item['sbelong'] = 0
            else:
                item['sbelong'] = 2
            # 标签
            keywords = list.xpath('./li[@class="biaoqian"]/text()').extract_first().split("：")[1]
            if not keywords.isdigit(): # 判断是否是"4"这样的数字，如果是就不赋值，取分类标签的第一项
                if keywords.find("["): #'[\"玄幻\"\"古风\"\"漫'
                    item['keywords'] = []
                    for key in keywords.split('""'):
                        key.replace("[","").replace('"',"").replace(']',"")
                        item['keywords'].append(key)
                    
                elif keywords.find(" "):#运动 神魔 玄幻 新作
                    item['keywords'] = keywords.split(" ") 
            #简介
            desc = list.xpath('./li[@class="info"]/text()').extract_first().split("简介：")[1]
            item['desc'] = desc
            #略缩图 链接 之后统一下载
            thum = list.xpath('./li[1]/a/img/@src').extract_first()
            item['thum'] = thum
            #详情链接 源头链接 /16041/" 漫画唯一id
            source_url = f'http://www.sixmh7.com{list.xpath("./li[1]/a/@href").extract_first()}'
            id = list.xpath("./li[1]/a/@href").extract_first().replace("/","")
            item['cartoonId'] = id
            item['sourceHref'] = source_url
    

            #todo 请求详情页面
            yield scrapy.Request(url = source_url, callback=self.parse_item_source, meta = {"item":item,"id":id})
            print(response.url)
            break;
        
    #! 获取详情 页面
    def parse_item_source(self, response):
        detail = response.xpath('//div[@class="cy_content2"]/div[2]')
        item = response.meta['item']
        #简介 判断两次简介长度进行赋值
        desc = detail.xpath('./div[@class="cy_info"]//p[@id="comic-description"]/text()').extract_first()
        if desc.find("：") <= 10 and desc.find("：") != -1: #武炼巅峰漫画： 去除冒号后面的东西，只需要简介
            desc = desc.split("：")[1]
        if len(desc) > len(item['desc']):
            item['desc'] = desc
        #作者
        author = detail.xpath('./div[@class="cy_info"]/div[1]//div[@class="cy_xinxi"]/span[1]/text()').extract_first().split("作者：")[1]
        if author.find(": ") <= 4 and author.find(": ") != -1:
            author = author.split("：")[1]
        item['author'] = author
        # 创建时间
        item["createTime"] = time.time()
        # 漫画属于分类
        classify = detail.xpath('./div[@class="cy_info"]/div[1]//div[4]/span[1]/text()').extract_first().split("类别：")[1]
        item['classify'] = classify
        # 爬取状态
        item['state'] = 0
        # 爬取的内容 ,内容是通过接口获取的值
        item['content'] = []
        item['weight'] = 1
        item['puTime'] = 0
        item['commentNum'] = 0
        item['cheart'] = 0
        item['ceye'] = 0
        # 最新章节
        LChapters_name = detail.xpath('./div[@class="cy_zhangjie"]/div[@class="cy_zhangjie_top"]/p[1]/a/text()').extract_first()
        url = detail.xpath('./div[@class="cy_zhangjie"]/div[@class="cy_zhangjie_top"]/p[1]/a/@href').extract_first()
        LChapters_url = f'http://www.sixmh7.com{url}'
        LChapters_time = detail.xpath('./div[@class="cy_zhangjie"]/div[@class="cy_zhangjie_top"]/p[2]/font/text()').extract_first()
            #将 2022-06-21 转换为时间戳
        timeArray = time.strptime(LChapters_time, "%Y-%m-%d") #转换成时间数组
        dic_time = time.mktime(timeArray) #转换成时间戳
        item['LChapters'] = {"updateTime":dic_time,"name":LChapters_name,"url":LChapters_url}
        
        #! 获取 content接口获取数据 POST 请求scrapy post 默认是x-www-form-urlencoded数据格式所以不要转换
        url = f'http://www.sixmh7.com/bookchapter/' 
        yield scrapy.FormRequest(url=url,formdata={"id":str(response.meta['id']),"id2":str(1)},callback=self.parse_bookChapter,meta={"item":item,"id":response.meta['id']})
    
    #! 3. 获取到章节数据
    def parse_bookChapter(self, response):
        item = response.meta['item']
        bookChapter = response.body
        bookChapter = json.loads(bookChapter)
        for chapter in bookChapter:
            chapter_url = f'http://www.sixmh7.com/{response.meta["id"]}/{chapter.chapterid}.html'
            chapter_data = {"id":chapter.chapterid,"name":chapter.chaptername, "sourceHref":chapter_url}
            yield scrapy.Request(url=chapter_url,callback=self.parse_bookChapter_detail,meta={"item":item,"chapter":chapter_data})
    
    #! 4. 访问详情页
    def parse_bookChapter_detail(self, response):
        img_data = self.parse_bookChapter_detail_img(response.text)

        #todo批量下载文件整合content, 存入数据库
        #? 1. 管道中下载图片

        #? 2. 保存content数据
        item = response.meta['item']
        chapter = response.meta['chapter']
        for url in img_data:
            img_sourceHref = url.rsplit("/")[1]
            chapter['sourceHref'] = img_sourceHref
        item['content'].append(chapter)
        yield item


    #!  获取漫画的详细信息 也就是看漫画页面, 发现可以在页面中找到响应的js，需要将js 执行得到图片数据
    # https://p3.byteimg.com/tos-cn-i-8gu37r9deh/80a4dd2a34e04a71a6ac714cc5c2f97f~noop.jpg
    def parse_bookChapter_detail_img(self, bookChapter_text):
        #todo 1.找到js代码提取出来
        regex = re.compile(r".*?eval(?P<javaScript>.*?)</script>",re.S)
        re_js_group = re.search(bookChapter_text)
        re_js = re_js_group.group('javaScript')

        #todo 2. 处理js代码，将执行结果输出，进行数据处理
        #? 将js变为自执行函数,并输出
        re_js_auto = re_js.replace("('g",")('g").replace("}))","})")
        re_js_auto = f'console.log({re_js_auto})'
        #? 将得到的js 字符串存入问题方便node执行，这里因为，这段js中有单双引号不能直接通过node执行
        #? 需要通过node -e require读取文件的方式执行， node -e "..." 执行字符串js
        with open("./index.js", mode="w") as f:
            f.write(re_js_auto)

        #执行node命令将结果输出，将输出结果字符串数组转换为python list
        cmd = 'node -e "require(\\"%s\\")"' % ('./index.js') #node -e "require(\"./index.js\")"
        pipeline = os.popen(cmd)
        result = pipeline.read().strip()
        # result = 'var newImgs=["https://p3.byteimg.com/tos-cn-i-8gu37r9deh/092b7dd1e0bb41c9bb37fc2cd5d1770a~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/6acc9f3e6f6342e58c265007b2dd7717~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/cf6296c57d1d47b9b209e3ec190f7a7f~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/4417f79a614f4bf2993c1ef36ae7f6cc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/bc6c32f704074086a40c106f9637c8b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d5ec578ec93f4154b4aa388572e6d57d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/54a904b9232b45bbbb794324d58e3f33~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/f8feea0ea88041a38353b024de4c54f9~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/2c5cc398c71c490f9c86df4a76b9ebdc~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/63a1a67347034915bc9d20643118932d~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/d9014265b0464a569ff0840f868942b1~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/7fefdd62d7744e16b888ac6e1e38dba3~noop.jpg","https://p3.byteimg.com/tos-cn-i-8gu37r9deh/80a4dd2a34e04a71a6ac714cc5c2f97f~noop.jpg"]'
        
        #? 最后将多余字符处理掉
        regex = re.compile(r"var newImgs=(?P<list>.*?)$", re.S)
        data = regex.search(result)
        data = json.loads(data.group('list'))
        return data

