# coding: utf8

"""
抓取豆瓣读书上关于互联网模块的所有评分超过8.5的推荐书籍
"""

import os
import re
import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup


# 伪装客户端
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"

# 正则匹配换行或者空格
replace_pattern = re.compile('\n|\s+')


class BookCrawler:
    def __init__(self):
        pass

    def get_book_list(self, category):
        """
        根据指定类别获取对应的书籍列表
        :param category: 分类
        :return:
        """
        page = 0
        while 1:
            print '正在处理第%d页' % (page + 1)
            url = 'http://book.douban.com/tag/%s?start=%d' % (category, page*20)
            refer = url
            buffers = StringIO()
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.USERAGENT, user_agent)
            curl.setopt(pycurl.REFERER, refer)
            curl.setopt(pycurl.WRITEDATA, buffers)
            curl.perform()
            curl.close()

            body = buffers.getvalue()
            soup = BeautifulSoup(body)

            content = soup.find('div', {'id': 'subject_list'})
            soup.decompose()
            # 这里用试探法测试页数
            clear_fix = content.find('div', {'class': 'clearfix'})
            if not clear_fix:
                break
            subject_list = content.find('ul', {'class': 'subject-list'}).findAll('li', {'class': 'subject-item'})
            target_list = []
            for item in subject_list:
                # 获取书名, 评分以及出版信息
                name = replace_pattern.sub('', item.find('h2').find('a').text)
                pub = replace_pattern.sub('', item.find('div', {'class': 'pub'}).text)
                # 处理少于10人评价的特殊情况
                rate_0 = item.find('div', {'class': 'star clearfix'}).find('span', {'class': 'rating_nums'})
                if not rate_0:
                    continue
                rates = replace_pattern.sub('', rate_0.text)
                target_list.append((name, rates, pub))
            file_name = '互联网%d' % (page + 1)
            page += 1
            self.write_to_file(target_list, 'out/', file_name)
        print('已处理完最后一页')

    def write_to_file(self, book_list, base_dir, file_name):
        """
        写入文件
        :param book_list: 目标书籍列表
        :param file_name: 文件名
        :return:
        """
        try:
            if not os.path.exists(base_dir):
                os.mkdir(base_dir)
            file_object = open(base_dir + file_name, 'w')
            for item in book_list:
                file_object.write('\t'.join(item).encode("utf8"))
                file_object.write('\n')
            file_object.close()
        except IOError:
            print('文件不存在')
            exit()