# -*- coding: utf-8 -*-
import os
# 切换至项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lib.crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()