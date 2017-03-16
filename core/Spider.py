#! env/bin/python
# coding:utf-8
import Queue
import re
import threading
from multiprocessing.pool import ThreadPool

import MySQLdb
import requests
import time
from bs4 import BeautifulSoup

from core.config import DB_CHARSET, DB_USER, DB_PASSWORD, DB_NAME
from core.config import DB_HOST, DB_PORT


class SpiderManager:

    __domain = None
    __url_queue = Queue.Queue(maxsize=0)
    __url_set = set()
    __lock = threading.Lock()
    __run = True
    __thread_num = 1
    __thread_pool = []
    __flag = 0
    __end_flag = __thread_num
    __child_domain = None
    __task_id = 0

    def __init__(self, task_id, url, thread_num=4):
        self.__task_id = task_id
        self.__thread_num = thread_num
        self.__end_flag = thread_num
        self.__url_queue.put(url)
        # self.__url_list.append(url)
        if url[-1] == '/':
            url = url[:-1]
        self.__domain = url.partition('//')
        self.__child_domain = set()

        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                               charset=DB_CHARSET)
        cursor = conn.cursor()
        # 后面可以将更新任务状态分离出类
        sql = 'update web_spider set target_domain="%s", spider_status=1 where task_id_id=%d' % (url, task_id)
        cursor.execute(sql)
        conn.commit()
        self.__cursor = cursor
        self.__conn = conn

        urls = self.read_robots()
        if urls is None:
            return
        for a_url in urls:
            url = ''.join(self.__domain) + a_url[1]
            self.__url_set.add(url)
            self.__url_queue.put(url)

    def read_robots(self):
        url = ''.join(self.__domain)+"/robots.txt"
        html = self.request(url)
        if html == '':
            return None
        urls = re.findall("(: )((https?:/)?/.*)", html)
        return urls

    def request(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.baidu.com/',
        }
        try:
            response = requests.get(url=url, headers=headers)
        except:
            print '访问该地址失败：', url
            return ''
        if response.status_code != 200:
            return ''
        head = response.headers
        head_lower = {}
        for (head_key, head_value) in head.items():
            head_key = head_key.lower()
            head_value = head_value.lower()
            head_key = unicode(head_key)
            head_value = unicode(head_value)
            head_lower[head_key] = head_value
        charset = ''
        try:
            # if 'content-type' in head_lower.keys():
            content_type = head_lower.get('content-type')
            if content_type.find('charset=') >= 0:
                charset = content_type.split("charset=")[1]
        except Exception as e:
            print e
        if charset == '':
            charset = 'utf-8'
        html = response.content.decode(charset)
        return html

    def start(self):
        for i in range(self.__thread_num):
            dic = {}
            dic['domain'] = self.__domain
            dic['url_queue'] = self.__url_queue
            dic['url_set'] = self.__url_set
            dic['lock'] = self.__lock
            dic['run'] = self.__run
            dic['flag'] = self.__flag
            dic['end_flag'] = self.__end_flag
            dic['child_domain'] = self.__child_domain
            t = SpiderThread(dic)
            t.start()
            self.__thread_pool.append(t)
        # monitor_thread = MonitorThread(dic)
        for t in self.__thread_pool:
            t.join()
        sql = 'update web_spider set spider_status=2 where task_id_id=%d' % self.__task_id
        self.__cursor.execute(sql)
        self.__conn.commit()
        self.__cursor.close()
        self.__conn.close()

    def stop(self):
        self.__lock.acquire()
        self.__run = False
        self.__lock.release()
        for t in self.__thread_pool:
            t.join()


class SpiderThread(threading.Thread):

    __url_queue = None
    __url_set = None
    __domain = None
    __lock = None
    __run = None
    __flag = None
    __end_flag = None
    __child_domain = None

    def __init__(self, dic):
        threading.Thread.__init__(self)
        self.__url_set = dic['url_set']
        self.__url_queue = dic['url_queue']
        self.__lock = dic['lock']
        self.__domain = dic['domain']
        self.__run = dic['run']
        self.__flag = dic['flag']
        self.__end_flag = dic['end_flag']
        self.__child_domain=dic['child_domain']

        self.__conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        self.__cursor = self.__conn.cursor()

    def run(self):
        while self.__run:
            if not self.__url_queue.empty():
                # 从任务队列获取url，加入集合和数据库,向queue添加url时已经保证了url没有重复。
                url = self.__url_queue.get()
                self.__lock.acquire()
                try:
                    sql = 'insert into web_url(domain, url, update_date) values("%s", "%s", now())' % (self.__domain[2], url)
                    self.__cursor.execute(sql)
                    self.__conn.commit()
                except:
                    pass
                # print url
                self.__url_set.add(unicode(url))
                self.__lock.release()
                # 爬取网页
                self.spider_url(url)
            else:
                self.__lock.acquire()
                self.__flag += 1
                if self.__flag >= 10:
                    self.__run = False
                self.__lock.release()
                time.sleep(0.1)
        self.__lock.acquire()
        self.__end_flag -= 1
        self.__lock.release()

    def spider_url(self, url):
        html = self.request(url)
        if html == '':
            return
        self.parse_html(html)

    def request(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.baidu.com/',
        }
        try:
            response = requests.get(url=url, headers=headers)
        except Exception as e:
            print '访问该地址失败', url
            return ''
        if response.status_code != 200:
            return ''
        head = response.headers
        head_lower = {}
        for (head_key, head_value) in head.items():
            head_key = head_key.lower()
            head_value = head_value.lower()
            head_key = unicode(head_key)
            head_value = unicode(head_value)
            head_lower[head_key] = head_value
        charset = ''
        try:
            # if 'content-type' in head_lower.keys():
            content_type = head_lower.get('content-type')
            if content_type.find('charset=') >= 0:
                charset = content_type.split("charset=")[1]
        except Exception as e:
            print e
        if charset == '':
            charset = 'utf-8'
        try:
            html = response.content.decode(charset)
        except:
            return ''
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # a href
        a_hrefs = soup.findAll('a')
        imgs = soup.findAll('img')
        links = soup.findAll('link')
        forms = soup.findAll('form')
        urls = set()
        statics = set()
        for a in a_hrefs:
            href = a.get("href")
            urls.add(href)
        for form in forms:
            action = form.get('action')
            urls.add(action)
        for img in imgs:
            src = img.get('src')
            statics.add(src)
        for link in links:
            href = link.get('href')
            statics.add(href)
        for href in urls:
            url = self.make_url(href)
            if url == '':
                continue
            self.__lock.acquire()
            if url not in self.__url_set:
                self.__url_set.add(url)
                self.__url_queue.put(url)
                # print url
            self.__lock.release()
        for static in statics:
            url = self.make_url(static)
            if url == '':
                continue
            self.__lock.acquire()
            if url not in self.__url_set:
                self.__url_set.add(url)
            self.__lock.release()

    def make_url(self, href):
        url = ''
        if href is None or href == '':
            return url
        if href.find("javascript:") >= 0:
            return url
        if href.find(self.__domain[2]) >= 0:
            url = ''.join(self.__domain) + href.split(self.__domain[2])[1]
        else:
            # 非本网站连接
            if href.find("//") >= 0:

                return url
            if href[0] == '/':
                url = ''.join(self.__domain) + href
            else:
                url = ''.join(self.__domain) + '/' + href
        return url


def new_spider(task_id, url, thread_num=4):
    spider_manager = SpiderManager(task_id, url, thread_num=thread_num)
    spider_manager.start()
    print 'spider end!'


if __name__ == '__main__':
    spider = SpiderManager("http://www.runoob.com/")
    spider.start()
    print 'spider end!'
