# Scrapy settings for nav project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from datetime import datetime
import os
BOT_NAME = 'nav'

SPIDER_MODULES = ['nav.spiders']
NEWSPIDER_MODULE = 'nav.spiders'

#让蜘蛛在访问网址中间休息1~2秒。
# DOWNLOAD_DELAY = 2
# RANDOMIZE_DOWNLOAD_DELAY = True

# 设置日志
# today = datetime.now()
# log_file_path = "logs/scrapy_{}_{}_{}.log".format(today.year, today.month, today.day)
# # # 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
# # LOG_LEVEL='DEBUG'
# LOG_FILE = log_file_path
# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')

# ----------------------
# LOG_STDOUT = True #该配置会影响 scrapyedweb 项目的读取 我搞了几天
# -----------------------------------------

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
}   
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
# LOG_LEVEL='ERROR'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nav (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# 这样子写linux 无法识别路径 需要使用os.sep自动识别window linux路径
# IMAGES_STORE = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'\static\images\cartoon')
IMAGES_STORE = os.path.join(os.path.dirname(os.path.dirname(__file__))+os.sep+'static'+os.sep+'images'+os.sep+'cartoon')

#mongodb数据库配置
DB_PORT = "27017"
DB_USER = "nav"
DB_PASSWORD = "123456"
DB_HOST = "127.0.0.1"


# 配置邮箱
MAIL_HOST = "smtp.qq.com" # 邮件发送服务器
MAIL_PORT = 465
MAIL_FROM = "815842080@qq.com"
MAIL_USER = "815842080@qq.com"
MAIL_PASS = "wouxqiiiohwzbfea"
MYEXT_ENABLED  = True
MAIL_SSL = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'nav.middlewares.NavSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'nav.middlewares.NavDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.corestats.CoreStats': None,  # 禁用默认的数据收集器
    'nav.CoreStats.SpiderOpenCloseLogging': 501,
    'nav.extendions.sendmail.SendEmail': 502,
}



# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'nav.pipelines.ImgsPipLine': 300,
    'nav.pipelines.MongodbPipeline': 301
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
