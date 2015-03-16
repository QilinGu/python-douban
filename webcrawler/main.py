# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lib.movie import MovieCrawler
from lib.book import BookCrawler

if __name__ == '__main__':
    # crawler = MovieCrawler()
    # crawler.run()
    BookCrawler().get_book_list('互联网')
    # BookCrawler().get_book_list('算法')
