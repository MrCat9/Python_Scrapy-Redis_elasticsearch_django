# telnet  https://baike.baidu.com/item/Telnet/810597?fr=aladdin
# 引自百度百科
# Telnet协议是TCP/IP协议族中的一员，是Internet远程登陆服务的标准协议和主要方式。
# 它为用户提供了在本地计算机上完成远程主机工作的能力。在终端使用者的电脑上使用telnet程序，用它连接到服务器。
# 终端使用者可以在telnet程序中输入命令，这些命令会在服务器上运行，就像直接在服务器的控制台上输入一样。
# 可以在本地就能控制服务器。要开始一个telnet会话，必须输入用户名和密码来登录服务器。
# Telnet是常用的远程控制Web服务器的方法。



# 你可以在cmd中监听spider中的变量。先要在控制面板中打开telnet客户端和服务端，在cmd中输入 telnet localhost 6023 即可。
# 打开telnet：控制面板\程序\程序和功能\启用或关闭Windows功能-->telnet客户端



# 测试telnet功能
# cmder下开启拉钩网的spider
C:\Users\admin
λ workon scrapy_test
C:\Users\admin
(scrapy_test) λ f:

F:\cmder\vendor\git-for-windows
(scrapy_test) λ cd F:\eclipse\···\···\test_scrapy_spider

F:\eclipse\···\···\test_scrapy_spider
(scrapy_test) λ scrapy crawl lagou

# cmd下开启telnet
C:\Users\admin>telnet localhost 6023

>>> est()  #查看当前spider的状态

>>> spider

>>> settings

>>> settings["COOKIES_ENABLED"]  #查看settings.py中的COOKIES_ENABLED

# Telnet终端(Telnet Console)文档  http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/telnetconsole.html  

# telnet源码  C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\scrapy\extensions\telnet.py
"""
Scrapy Telnet Console extension

See documentation in docs/topics/telnetconsole.rst
"""

import pprint
import logging

from twisted.internet import protocol
try:
    from twisted.conch import manhole, telnet
    from twisted.conch.insults import insults
    TWISTED_CONCH_AVAILABLE = True
except ImportError:
    TWISTED_CONCH_AVAILABLE = False

from scrapy.exceptions import NotConfigured
from scrapy import signals
from scrapy.utils.trackref import print_live_refs
from scrapy.utils.engine import print_engine_status
from scrapy.utils.reactor import listen_tcp

try:
    import guppy
    hpy = guppy.hpy()
except ImportError:
    hpy = None

logger = logging.getLogger(__name__)

# signal to update telnet variables
# args: telnet_vars
update_telnet_vars = object()


class TelnetConsole(protocol.ServerFactory):

    def __init__(self, crawler):
        if not crawler.settings.getbool('TELNETCONSOLE_ENABLED'):
            raise NotConfigured
        if not TWISTED_CONCH_AVAILABLE:
            raise NotConfigured
        self.crawler = crawler
        self.noisy = False
        self.portrange = [int(x) for x in crawler.settings.getlist('TELNETCONSOLE_PORT')]
        self.host = crawler.settings['TELNETCONSOLE_HOST']
        self.crawler.signals.connect(self.start_listening, signals.engine_started)
        self.crawler.signals.connect(self.stop_listening, signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start_listening(self):
        self.port = listen_tcp(self.portrange, self.host, self)
        h = self.port.getHost()
        logger.debug("Telnet console listening on %(host)s:%(port)d",
                     {'host': h.host, 'port': h.port},
                     extra={'crawler': self.crawler})

    def stop_listening(self):
        self.port.stopListening()

    def protocol(self):
        telnet_vars = self._get_telnet_vars()
        return telnet.TelnetTransport(telnet.TelnetBootstrapProtocol,
            insults.ServerProtocol, manhole.Manhole, telnet_vars)

    def _get_telnet_vars(self):
        # Note: if you add entries here also update topics/telnetconsole.rst
        telnet_vars = {
            'engine': self.crawler.engine,
            'spider': self.crawler.engine.spider,
            'slot': self.crawler.engine.slot,
            'crawler': self.crawler,
            'extensions': self.crawler.extensions,
            'stats': self.crawler.stats,
            'settings': self.crawler.settings,
            'est': lambda: print_engine_status(self.crawler.engine),
            'p': pprint.pprint,
            'prefs': print_live_refs,
            'hpy': hpy,
            'help': "This is Scrapy telnet console. For more info see: " \
                "https://doc.scrapy.org/en/latest/topics/telnetconsole.html",
        }
        self.crawler.signals.send_catch_log(update_telnet_vars, telnet_vars=telnet_vars)
        return telnet_vars
