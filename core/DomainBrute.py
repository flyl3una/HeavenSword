# env/bin/python
# coding:utf-8
import os
import socket
import threading
from multiprocessing.pool import ThreadPool

import dns.resolver
import dns.query
import re
import requests

from HeavenSword.settings import MODEL_PATH


class DomainBrute:

    __father_domain = None
    __option = None
    __dict = []
    __thread_num = 4
    __domain_dic = {}
    __lock = threading.Lock()
    __current_index = 0
    __run = True

    def __init__(self, father_domain, option='useually', thread_num=4):
        self.__father_domain = father_domain
        self.__option = option
        self.__thread_num = thread_num
        socket.setdefaulttimeout(0.5)

    def load_dict(self):
        dict_name = ''
        if self.__option == 'useually':
            dict_name = MODEL_PATH + os.sep + 'dict' + os.sep + 'domain_subnames.txt'
        elif self.__option == 'all':
            dict_name = MODEL_PATH + os.sep + 'dict' + os.sep + 'domain_subnames_full.txt'
        dict_file = file(dict_name)
        for line in dict_file:
            if line not in self.__dict:
                line = line.strip()
                self.__dict.append(line)

    def start(self):
        pool = ThreadPool(processes=self.__thread_num)
        pool.map(self.check_domain, self.__dict)

    def check_domain(self, sub_domain):
        domain = sub_domain + '.' + self.__father_domain
        # domain = 'www.baidu.com'
        try:
            res = socket.getaddrinfo(domain, None)
            addrs = []
            for i in res:
                addr = i[4][0]
                addrs.append(addr)
                print domain, addr
            self.__lock.acquire()
            self.__current_index += 1
            self.__domain_dic[domain] = addrs
            self.__lock.release()
        except dns.resolver.NoNameservers as e:
            print e.message
        except Exception, e:
            pass

    def percent(self):
        return self.__current_index


# 没有递归爆破
if __name__ == '__main__':
    domain = 'runboo.com'
    domainBrute = DomainBrute(domain, thread_num=2)
    domainBrute.load_dict()
    domainBrute.start()
    print 'domain brute'