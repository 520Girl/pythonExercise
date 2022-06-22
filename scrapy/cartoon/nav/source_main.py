# 启动多个爬虫项目
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 在Scrapy框架内控制爬虫
if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    
	# 控制台主界面
    main = int(input("请输入爬取网站：（1为site01 2为site02 3为site03）"))
    if main == 1:
        process.crawl("site01_spider")
    elif main == 2:
        process.crawl("site02_spider")
    elif main == 3:
        process.crawl("site03_spider")
    else:
        print("输入错误！")
        pass

    print('-----爬虫启动-----')
    process.start()
