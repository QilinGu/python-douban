# coding: utf8

"""
抓取豆瓣电影top250资源
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
refer_url = "http://movie.douban.com"

# 正则匹配换行或者空格
replace_pattern = re.compile('\n|\s+')


class TopMovieCrawler:
    def __init__(self):
        pass

    def get_top_movie_list(self, source_url):
        """
        拿到推荐的250部经典电影列表
        :param source_url: 源网址
        :return:
        """
        curl = pycurl.Curl()
        curl.setopt(pycurl.USERAGENT, user_agent)
        curl.setopt(pycurl.REFERER, refer_url)

        page = 0
        extra_url = ""
        target_list = []

        while 1:
            print '正在处理第%d页' % (page + 1)
            target_url = source_url + extra_url
            buffers = StringIO()
            curl.setopt(pycurl.URL, target_url)
            curl.setopt(pycurl.WRITEDATA, buffers)
            curl.perform()

            body = buffers.getvalue()
            buffers.close()
            soup = BeautifulSoup(body, "html.parser")
            content = soup.find('div', {'id': 'content'})
            soup.decompose()
            clear_fix = content.find('div', {'class': 'article'})
            subject_list = clear_fix.find('ol', {'class': 'grid_view'}).findAll('li')
            # 这里用试探法测试页数
            if not subject_list:
                break
            for item in subject_list:
                # 获取电影名称, 评分
                name = replace_pattern.sub('', item.find('div', {'class': 'hd'}).find('a').text)
                # 处理少于10人评价的特殊情况
                rate_0 = item.find('div', {'class': 'star'}).find('span', {'class': 'rating_num'})
                if not rate_0:
                    continue
                rates = replace_pattern.sub('', rate_0.text)
                target_list.append((name, rates))

            page += 1
            extra_url = "?start=%d&filter=" % (25 * page)

        print('已处理完最后一页')
        curl.close()
        file_name = '%s.txt' % u"top250电影集合"
        self.write_to_file(target_list, u"top250电影/", file_name)

    def write_to_file(self, movie_list, category_dir, file_name):
        """
        写入文件
        :param movie_list: 目标书籍列表
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
            for item in movie_list:
                file_object.write('\t'.join(item).encode("utf8"))
                file_object.write('\n')
            file_object.close()
        except IOError:
            print('文件不存在')
            exit()
