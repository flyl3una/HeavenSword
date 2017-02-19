#! env/bin/python
# coding:utf-8
import re

import requests
import json

from bs4 import BeautifulSoup


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

    def __init__(self, url=None, apps=None):
        self.__url = url
        self.__apps = apps

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
        print '-----------------------head------------------------'
        print head_lower
        content_type = head_lower.get('content-type')
        # print '-----------------------charset----------------------'
        try:
            # charset_index = content_type.index('charset=')
            # charset = content_type[charset_index + 8:]
            charset = content_type.split("charset=")[1]
        except Exception as e:
            print e
        # print charset
        html = response.content.decode(charset)
        print '-----------------------html------------------------'
        print html

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
        '''
        cate:app类型
        meta和headers能获取到版本信息
        meta:meta信息
        website:app官网
        implies：语言或者app框架

        env/header/html/meta/script/url任意匹配中一个就行,匹配到之后取得cate id，根据category获取多个内容

        head的Server里面包含服务器或者语言。
        :return:
        '''
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
                pass
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

if __name__ == '__main__':
    print 'finger'
    json_file_path = '../setting/apps.json'
    apps = getApps(json_file_path)
    finger = WebFinger('https://zh-cn.wordpress.com/', apps)
    ret = finger.request()
    if ret == '[ERROR]: target url is None':
        print 'error'
    finger.analyse()
    finger.show_result()
    result = finger.get_finger_list()
    print '-----------------finger json----------------'
    print json.dumps(result)