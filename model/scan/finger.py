#! env/bin/python
#coding:utf-8
import requests


def getJson():
    return None


class WebAppFinger:

    __target = None
    __html = None
    __head = None

    def __init__(self, target=None):
        self.__target = target


    def request(self):
        if self.__target is None:
            return '[ERROR]: target is None'
        ret = False
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.baidu.com/',
        }
        response = requests.get(url=self.__target, headers=headers)
        head = response.headers
        print '-----------------------head------------------------'
        print head
        content_type = head.get('content-type')
        print '-----------------------charset----------------------'
        try:
            charset_index = content_type.index('charset=')
            charset = content_type[charset_index+8:]
        except Exception as e:
            print e
        print charset
        html = response.content.decode(charset)
        print '-----------------------html------------------------'
        print html

        self.__html = html
        self.__head = head


if __name__ == '__main__':
    print 'finger'
    finger = WebAppFinger('https://zh-cn.wordpress.com/')
    ret = finger.request()
    if ret == '[ERROR]: target is None':
        print 'error'
