import scrapy
from downloadImage.items import  DownloadimageItem


class DimageSpider(scrapy.Spider):
    name = 'dImage'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    def parse(self, response):
        dow =[
            {
        "sourceHref":"https://p3.byteimg.com/origin/ffbc0002b033d6f76f81",
        "content":[{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/71545a8a88e340439344cf0a22a0f518~noop.jpg",
            "name":"父陈子1"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/c0ff5c278a1a4c9d9a100960e5ac2053~noop.jpg",
            "name":"父陈子2"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/724837141f634adb9bdda6d7af3792c0~noop.jpg",
            "name":"父陈子3"
        }]
        },{
        "sourceHref":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/a352a24b28194c29ac3a9ed2929afc98~noop.jpg",
        "content":[{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/35fcc182d6be479192121506c8fea038~noop.jpg",
            "name":"末世1"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/cd95feb5a51d4348b4e57d38b3918646~noop.jpg",
            "name":"末世2"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/1bc0ad593f2b4ce78a54a801481a3ee7~noop.jpg",
            "name":"末世3"
        }]
        }
        ]
        item = DownloadimageItem()
        item['files'] = 'files'
        item['doc'] = dow
        item['image_urls'] = [
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/a179768b71e645b187421ae0abc3b740~noop.jpg',
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/ede2db674fc9446f98253c161b76a530~noop.jpg',
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/5c21474b115b456fbb266dc75223855e~noop.jpg'
            ]
        yield item
    

