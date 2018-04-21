# 扩展(Extensions)  文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/extensions.html
# 摘自 http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/extensions.html
# 扩展框架提供一个机制，使得你能将自定义功能绑定到Scrapy。
# 扩展只是正常的类，它们在Scrapy启动时被实例化、初始化。

# 扩展  通过信号量绑定处理函数-->什么信号触发时，执行什么操作



# middlewares和pipelines可以理解为扩展



# http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/extensions.html 上extensions的示例
# 摘自 http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/extensions.html
# 扩展例子(Sample extension)
# 这里我们将实现一个简单的扩展来演示上面描述到的概念。 该扩展会在以下事件时记录一条日志：

# spider被打开
# spider被关闭
# 爬取了特定数量的条目(items)
# 该扩展通过 MYEXT_ENABLED 配置项开启， items的数量通过 MYEXT_ITEMCOUNT 配置项设置。

# 以下是扩展的代码:

from scrapy import signals
from scrapy.exceptions import NotConfigured

class SpiderOpenCloseLogging(object):

    def __init__(self, item_count):
        self.item_count = item_count

        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise

        # NotConfigured otherwise

        if not crawler.settings.getbool('MYEXT_ENABLED'):

            raise NotConfigured

        # get the number of items from settings

        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object

        ext = cls(item_count)

        # connect the extension object to signals  #绑定信号

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object

        return ext

    def spider_opened(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        spider.log("closed spider %s" % spider.name)

    def item_scraped(self, item, spider):
        self.items_scraped += 1

        if self.items_scraped % self.item_count == 0:
            spider.log("scraped %d items" % self.items_scraped)



# extensions实例
# C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\extensions\corestats.py
"""
Extension for collecting core stats like items scraped and start/finish times
"""
import datetime

from scrapy import signals

class CoreStats(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)  #绑定信号
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)  #spider_closed时，执行spider_closed函数
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.response_received, signal=signals.response_received)
        return o

    def spider_opened(self, spider):
        self.stats.set_value('start_time', datetime.datetime.utcnow(), spider=spider)

    def spider_closed(self, spider, reason):
        self.stats.set_value('finish_time', datetime.datetime.utcnow(), spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)

    def item_scraped(self, item, spider):
        self.stats.inc_value('item_scraped_count', spider=spider)

    def response_received(self, spider):
        self.stats.inc_value('response_received_count', spider=spider)

    def item_dropped(self, item, spider, exception):
        reason = exception.__class__.__name__
        self.stats.inc_value('item_dropped_count', spider=spider)
        self.stats.inc_value('item_dropped_reasons_count/%s' % reason, spider=spider)



# extensions实例
# C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\extensions\memusage.py
"""
MemoryUsage extension

See documentation in docs/topics/extensions.rst
"""
import sys
import socket
import logging
from pprint import pformat
from importlib import import_module

from twisted.internet import task

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender
from scrapy.utils.engine import get_engine_status

logger = logging.getLogger(__name__)


class MemoryUsage(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('MEMUSAGE_ENABLED'):
            raise NotConfigured
        try:
            # stdlib's resource module is only available on unix platforms.
            self.resource = import_module('resource')
        except ImportError:
            raise NotConfigured

        self.crawler = crawler
        self.warned = False
        self.notify_mails = crawler.settings.getlist('MEMUSAGE_NOTIFY_MAIL')
        self.limit = crawler.settings.getint('MEMUSAGE_LIMIT_MB')*1024*1024
        self.warning = crawler.settings.getint('MEMUSAGE_WARNING_MB')*1024*1024
        self.check_interval = crawler.settings.getfloat('MEMUSAGE_CHECK_INTERVAL_SECONDS')
        self.mail = MailSender.from_settings(crawler.settings)
        crawler.signals.connect(self.engine_started, signal=signals.engine_started)  #绑定信号
        crawler.signals.connect(self.engine_stopped, signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def get_virtual_size(self):
        size = self.resource.getrusage(self.resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            # on Mac OS X ru_maxrss is in bytes, on Linux it is in KB
            size *= 1024
        return size

    def engine_started(self):
        self.crawler.stats.set_value('memusage/startup', self.get_virtual_size())
        self.tasks = []
        tsk = task.LoopingCall(self.update)
        self.tasks.append(tsk)
        tsk.start(self.check_interval, now=True)
        if self.limit:
            tsk = task.LoopingCall(self._check_limit)
            self.tasks.append(tsk)
            tsk.start(self.check_interval, now=True)
        if self.warning:
            tsk = task.LoopingCall(self._check_warning)
            self.tasks.append(tsk)
            tsk.start(self.check_interval, now=True)

    def engine_stopped(self):
        for tsk in self.tasks:
            if tsk.running:
                tsk.stop()

    def update(self):
        self.crawler.stats.max_value('memusage/max', self.get_virtual_size())

    def _check_limit(self):
        if self.get_virtual_size() > self.limit:
            self.crawler.stats.set_value('memusage/limit_reached', 1)
            mem = self.limit/1024/1024
            logger.error("Memory usage exceeded %(memusage)dM. Shutting down Scrapy...",
                         {'memusage': mem}, extra={'crawler': self.crawler})
            if self.notify_mails:
                subj = "%s terminated: memory usage exceeded %dM at %s" % \
                        (self.crawler.settings['BOT_NAME'], mem, socket.gethostname())
                self._send_report(self.notify_mails, subj)
                self.crawler.stats.set_value('memusage/limit_notified', 1)

            open_spiders = self.crawler.engine.open_spiders
            if open_spiders:
                for spider in open_spiders:
                    self.crawler.engine.close_spider(spider, 'memusage_exceeded')
            else:
                self.crawler.stop()

    def _check_warning(self):
        if self.warned: # warn only once
            return
        if self.get_virtual_size() > self.warning:
            self.crawler.stats.set_value('memusage/warning_reached', 1)
            mem = self.warning/1024/1024
            logger.warning("Memory usage reached %(memusage)dM",
                           {'memusage': mem}, extra={'crawler': self.crawler})
            if self.notify_mails:
                subj = "%s warning: memory usage reached %dM at %s" % \
                        (self.crawler.settings['BOT_NAME'], mem, socket.gethostname())
                self._send_report(self.notify_mails, subj)
                self.crawler.stats.set_value('memusage/warning_notified', 1)
            self.warned = True

    def _send_report(self, rcpts, subject):
        """send notification mail with some additional useful info"""
        stats = self.crawler.stats
        s = "Memory usage at engine startup : %dM\r\n" % (stats.get_value('memusage/startup')/1024/1024)
        s += "Maximum memory usage           : %dM\r\n" % (stats.get_value('memusage/max')/1024/1024)
        s += "Current memory usage           : %dM\r\n" % (self.get_virtual_size()/1024/1024)

        s += "ENGINE STATUS ------------------------------------------------------- \r\n"
        s += "\r\n"
        s += pformat(get_engine_status(self.crawler.engine))
        s += "\r\n"
        self.mail.send(rcpts, subject, s)




