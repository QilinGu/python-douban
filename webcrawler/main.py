# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lib.crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()