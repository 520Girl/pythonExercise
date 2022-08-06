import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender
logger = logging.getLogger(__name__)
class SendEmail(object):

    def __init__(self,sender,crawler):
        self.sender = sender
        self.crawler = crawler
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        smtphost = crawler.settings.get('MAIL_HOST') # 发送邮件的服务器
        mailfrom = crawler.settings.get('MAIL_FROM') 
        smtpport = crawler.settings.get('MAIL_PORT') # 邮件端口
        smtpuser = crawler.settings.get('MAIL_USER') # 邮件发送者用户名
        smtppass = crawler.settings.get('MAIL_PASS') # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
        smtpssl = crawler.settings.get('MAIL_SSL')

        sender = MailSender(smtphost=smtphost,smtpuser=smtpuser,mailfrom=mailfrom,smtppass=smtppass,smtpport=smtpport,smtpssl=smtpssl) #由于这里邮件的发送者和邮件账户是同一个就都写了mail_user了
        h = cls(sender,crawler)

        return h

    def spider_idle(self,spider):
        logger.info('idle spider %s' % spider.name)

    def spider_closed(self, spider, reason):
        
        stats_info = self.crawler.stats._stats  # 爬虫结束时控制台信息
        logger.info("closed spider %s", spider.name)
        body = 'spider [%s] is closed，原因：%s.\n以下为运行信息：\n %s' % (spider.name, reason, stats_info)
        if hasattr(self.crawler.spider,'input_cartoon_name'):
            subject = '%s 更新漫画' % self.crawler.spider.input_cartoon_name
            body +='\n更新数据为: %s' % self.crawler.spider.update_data
            return self .sender.send(to={'815842080@qq.com'}, subject=subject, body=body)

        elif len(self.crawler.spider.update_data) != 0 and len(self.crawler.spider.crawler_data) != 0: # 表示当更新和爬虫漫画并存是，也就是6cartoon具有的功能
            subject = '%s 更新漫画' % self.crawler.spider.input_cartoon_name
            body +='\n更新数据为: %s \n' % self.crawler.spider.update_data
            body +='\n创建数据为: %s \n' % self.crawler.spider.crawler_data
            return self .sender.send(to={'815842080@qq.com'}, subject=subject, body=body)

        elif len(self.crawler.spider.update_data) != 0 : #只有更新漫画
            subject = '更新漫画'
            body +='\n更新数据为: %s' % self.crawler.spider.update_data
            return self .sender.send(to={'815842080@qq.com'}, subject=subject, body=body)

        else: #只有创建漫画
            subject = '创建漫画'
            body +='\n创建数据为: %s' % self.crawler.spider.crawler_data
            return self .sender.send(to={'815842080@qq.com'}, subject=subject, body=body)
        # self.sender.send(to={'zfeijun@foxmail.com'}, subject=subject, body=body)
