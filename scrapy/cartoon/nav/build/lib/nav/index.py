from scrapy.cmdline import execute
import os
# 获取当前文件路径
dirpath = os.path.dirname(os.path.abspath(__file__))
#切换到scrapy项目路径下
os.chdir(dirpath[:dirpath.rindex("\\")])
# 启动爬虫,第三个参数为爬虫name
# print(os.path.join(os.path.dirname(os.path.dirname(__file__)),r'static\images\cartoon'))
execute(['scrapy','crawl','6cartoon'])
# execute(['scrapy','crawl','baozimh'])

