# coding: utf8

"""
抓取豆瓣读书上关于互联网模块的所有评分超过8.5的推荐书籍
"""

import os
import re
import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup


# 伪装成iPad客户端
user_agent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) ' \
             'AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# 伪造来源地址
refer_url = "http://book.douban.com"

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
        curl = pycurl.Curl()
        curl.setopt(pycurl.USERAGENT, user_agent)
        curl.setopt(pycurl.REFERER, refer_url)

        page = 0
        while 1:
            print '正在处理第%d页' % (page + 1)
            url = 'http://book.douban.com/tag/%s?start=%d' % (category, page * 20)
            buffers = StringIO()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.WRITEDATA, buffers)
            curl.perform()

            body = buffers.getvalue()
            buffers.close()
            soup = BeautifulSoup(body, "html.parser")

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
                # 抓取评分高于8.5的书籍
                if float(rates) > 8.5:
                    target_list.append((name, rates, pub))
            file_name = '%s%d.txt' % (category, page + 1)
            page += 1
            self.write_to_file(target_list, '%s/' % category, file_name)

        curl.close()
        print('已处理完最后一页')

    def write_to_file(self, book_list, category_dir, file_name):
        """
        写入文件
        :param book_list: 目标书籍列表
        :param category_dir: 归档目录
        :param file_name: 文件名
        :return:
        """
        try:
            base_dir = 'out/'
            if not os.path.exists(base_dir):
                os.mkdir(base_dir)
            if not os.path.exists(base_dir + category_dir):
                os.mkdir(base_dir + category_dir)
            file_object = open(base_dir + category_dir + file_name, 'w')
            for item in book_list:
                file_object.write('\t'.join(item).encode("utf8"))
                file_object.write('\n')
            file_object.close()
        except IOError:
            print('文件不存在')
            exit()
