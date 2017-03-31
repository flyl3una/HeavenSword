#! env/bin/python
# coding:utf-8
import os
import re

import MySQLdb
import requests
import json

from bs4 import BeautifulSoup

from HeavenSword.settings import WEB_PATH
from tools.config import FINGER_PATH, DB_HOST, DB_CHARSET, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from tools.function import get_domain


def getApps(path):
    fp = file(path)
    app_dic = json.load(fp, encoding='utf-8')
    return app_dic


class WebFinger:
    __url = None
    __html = None
    __head = None
    __apps = None
    __charset = 'utf-8'
    __result = []
    __finger_list=[]

    def __init__(self, url=None, apps=None, finger_id=0):
        self.__url = url
        self.__apps = apps
        self.__finger_id = finger_id

    def request(self):
        if self.__url is None:
            return '[ERROR]: target url is None'
        ret = False
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.baidu.com/',
        }
        response = requests.get(url=self.__url, headers=headers)
        head = response.headers
        head_lower = {}
        for (head_key, head_value) in head.items():
            head_key = head_key.lower()
            head_value = head_value.lower()
            head_key = unicode(head_key)
            head_value = unicode(head_value)
            head_lower[head_key] = head_value
        # print '-----------------------head------------------------'
        # print head_lower
        content_type = head_lower.get('content-type')
        # print '-----------------------charset----------------------'
        try:
            # charset_index = content_type.index('charset=')
            # charset = content_type[charset_index + 8:]
            charset = content_type.split("charset=")[1]
        except Exception as e:
            conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
            cursor = conn.cursor()
            sql = 'update web_finger set status=31 where id=%d' % self.__finger_id
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            print e
        # print charset
        html = response.content.decode(charset)
        # print '-----------------------html------------------------'
        # print html

        self.__charset = charset
        self.__html = html
        self.__head = head_lower

    def matching(self, content, regex):
        matched = False
        regex, _, rest = regex.partition('\\;')
        # regex = str(regex)
        # content = str(content)
        try:
            if re.search(regex, content, re.IGNORECASE):
            # pattern = re.compile(regex)
            # if pattern.search(content, re.IGNORECASE):#re.IGNORECASE忽略大小写
                matched = True
        except Exception, e:
            print e
        return matched

    def matchItem(self, content, items):
        matched = False
        if type(items) == list:
            for item in items:
                matched = self.matching(content, item)
                if matched:
                    break
        # elif type(items) == str:
        else:
            matched = self.matching(content, items)
        return matched

    def matchMetas(self, content, metas):
        matched = False
        soup = BeautifulSoup(content, 'html.parser')
        for (meta_key, meta_value) in metas.items():
            meta_value, _, rest = meta_value.partition('\\;')
            matched = soup.findAll(name='meta', attrs={meta_key:re.compile(meta_value)})
            if matched:
                break
        return matched

    #匹配script还存在问题
    def analyse(self):
        """
        cate:app类型
        meta和headers能获取到版本信息
        meta:meta信息
        website:app官网
        implies：语言或者app框架

        env/header/html/meta/script/url任意匹配中一个就行,匹配到之后取得cate id，根据category获取多个内容

        head的Server里面包含服务器或者语言。
        :return:
        """

        conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='HeavenSword',
                               charset='utf8')
        cursor = conn.cursor()

        index = 0
        for name, app in self.__apps[u'apps'].items():
            # for key, obj in app.items():
            keys = app.keys()
            url, html, headers, meta, env, script, implies = False, False, False, False, False, False, False
            if u'meta' in keys:

                meta = self.matchMetas(self.__html, app[u'meta'])
                    # 获取版本号
                    # if meta_i.index('version'):
                    #     pass

            if u'headers' in keys:
                for (header_key, header_value) in app[u'headers'].items():
                    header_key = header_key.lower()
                    if header_key not in self.__head:
                        continue
                    headers = self.matching(self.__head[header_key], header_value)
                    if headers:
                        break

            if u'implies' in keys:
                implies = True

            if u'url' in keys:
                url = self.matchItem(self.__html, app[u'url'])

            if u'html' in keys:
                html = self.matchItem(self.__html, app[u'html'])

            # 匹配script还有问题，可能会匹配不到。
            if u'script' in keys:
                script = self.matchItem(self.__html, app[u'script'])

            # if u'env' in keys:
            #     env = self.match_item(self.__html, app[u'env'])
            #     pass
            if url or html or script or headers or env or meta:
                result = {}
                imp = []
                result[u'cats_id'] = app[u'cats']#是数组
                result[u'name'] = name
                if implies:
                    if type(app[u'implies']) == list:
                        imp += app[u'implies']
                    # if type(app[u'implies']) == unicode:
                    else:
                        imp.append(app[u'implies'])
                if imp != []:
                    result['implies'] = imp
                self.__result.append(result)
            index += 1
            sql = 'update web_finger set current_index=%d where id=%d' % (index, self.__finger_id)
            cursor.execute(sql)
            conn.commit()

        cursor.close()
        conn.close()

    def show_result(self):
        for i in self.__result:
            cats = i[u'cats_id']
            for id in cats:
                s = self.__apps[u'categories'][str(id)]+': '+i[u'name']
                if 'implies' in i:
                    for implies in i['implies']:
                        s += '['+implies+']'
                # print self.__apps[u'categories'][str(id)], ':', i[u'name']
                print s

    def get_finger_list(self):
        for result in self.__result:
            finger = {}
            cats_id = result[u'cats_id']
            cats = []
            for id in cats_id:
                # s = self.__apps[u'categories'][str(id)] + ': ' + result[u'name']
                cats.append(self.__apps[u'categories'][unicode(id)])
            finger['cats'] = cats
            finger['name'] = result[u'name']
            implies = []
            if 'implies' in result:
                for implies_res in result['implies']:
                    # s += '[' + implies + ']'
                    implies.append(implies_res)
                # print self.__apps[u'categories'][str(id)], ':', i[u'name']
            finger['implies'] = implies
            self.__finger_list.append(finger)
        return self.__finger_list


def get_finger(finger_id, url):
    json_file_path = os.path.join(FINGER_PATH, 'apps.json')
    # 获取指纹json字典
    apps = getApps(json_file_path)

    conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    cursor = conn.cursor()

    finger_count = len(apps[u'apps'])
    sql = 'update web_finger set finger_count=%d, status=1 where id=%d' % (finger_count, finger_id)
    cursor.execute(sql)
    # commit提交后才会执行该sql语句
    conn.commit()

    finger = WebFinger(url, apps, finger_id=finger_id)
    ret = finger.request()
    if ret == '[ERROR]: target url is None':
        return 'error'
    finger.analyse()
    finger.show_result()
    result = finger.get_finger_list()
    # json_result = json.dumps(result)
    print result

    sql = 'select target_domain from web_finger where id=%d' % finger_id
    cursor.execute(sql)
    target_domain = cursor.fetchone()
    # domain = get_domain(target_url[0])
    domain = target_domain[0]
    for i in result:
        cats = i[u'cats']
        name = i[u'name']
        for cat in cats:
            if 'implies' in i:
                for implies in i['implies']:
                    sql = 'insert into web_apptype(domain, name, cata, implies, update_date) values("%s", "%s", "%s", "%s", now())' % (domain, name, cat, implies)
                    cursor.execute(sql)
                    # conn.commit()

    #状态设置为2，完成
    sql = 'update web_finger set status=2 where id=%d' % finger_id
    cursor.execute(sql)
    # commit保证缓冲区中的sql语句先执行后才进行后面的操作，防止多个sql语句同时执行导致出错
    conn.commit()
    # 数据库使用完后一定要关闭连接。
    cursor.close()
    conn.close()
    print '指纹识别完成'
    # print result
    # return result


def get_finger1(target_url):
    json_file_path = os.path.join(FINGER_PATH, 'apps.json')
    # 获取指纹json字典
    apps = getApps(json_file_path)
    finger = WebFinger(target_url, apps)
    ret = finger.request()
    if ret == '[ERROR]: target url is None':
        return 'error'
    finger.analyse()
    finger.show_result()
    result = finger.get_finger_list()

if __name__ == '__main__':
    # print 'finger'
    json_file_path = os.path.join(FINGER_PATH, 'apps.json')
    apps = getApps(json_file_path)
    finger = WebFinger('https://zh-cn.wordpress.com/', apps)
    ret = finger.request()
    if ret == '[ERROR]: target url is None':
        print 'error'
    finger.analyse()
    finger.show_result()
    result = finger.get_finger_list()
    # print '-----------------finger json----------------'
    # print json.dumps(result)