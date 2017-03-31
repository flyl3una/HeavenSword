# env/bin/python
# coding:utf-8
import os
import socket
import threading
from multiprocessing.pool import ThreadPool

import MySQLdb
import dns.resolver
import dns.query
import re
import requests

from tools.config import DICT_PATH, DB_HOST, DB_CHARSET, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


class DomainBrute:

    __father_domain = None
    __option = None
    __dict = []
    __thread_num = 4
    __domain_dic = {}
    __lock = threading.Lock()
    __current_index = 0
    __run = True
    __task_id = 0

    def __init__(self, domain_brute_id, father_domain, option='usually', thread_num=4):
        self.__domain_brute_id = domain_brute_id
        self.__father_domain = father_domain
        self.__option = option
        self.__thread_num = thread_num
        socket.setdefaulttimeout(0.3)
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                               charset=DB_CHARSET)
        cursor = conn.cursor()
        sql = 'update web_domainbrute set status=1, thread=%d where id=%d' % (thread_num, domain_brute_id)
        cursor.execute(sql)
        conn.commit()
        self.__conn = conn
        self.__cursor = cursor

    def load_dict(self):
        dict_name = ''
        if self.__option == 'usually':
            dict_name = os.path.join(DICT_PATH, 'domain_subnames.txt')
        elif self.__option == 'all':
            dict_name = os.path.join(DICT_PATH, 'domain_subnames_full.txt')
        dict_file = file(dict_name)
        count = 0
        for line in dict_file:
            if line not in self.__dict:
                line = line.strip()
                self.__dict.append(line)
                count += 1
        sql = 'update web_domainbrute set domain_count=%d where id=%d' % (count, self.__domain_brute_id)
        self.__cursor.execute(sql)
        self.__conn.commit()

    def start(self):
        pool = ThreadPool(processes=self.__thread_num)
        pool.map(self.check_domain, self.__dict)
        sql = 'update web_domainbrute set status=2 where id=%d' % self.__domain_brute_id
        self.__cursor.execute(sql)
        self.__conn.commit()
        self.__cursor.close()
        self.__conn.close()

    def check_domain(self, sub_domain):
        domain = sub_domain + '.' + self.__father_domain
        # domain = 'www.baidu.com'
        try:
            self.__lock.acquire()
            self.__current_index += 1
            sql = 'update web_domainbrute set current_index=%d where id=%d' % (self.__current_index, self.__domain_brute_id)
            self.__cursor.execute(sql)
            self.__conn.commit()
            self.__lock.release()
            res = socket.getaddrinfo(domain, None)
            addrs = []
            for i in res:
                addr = i[4][0]
                addrs.append(addr)
            # print domain, addr
            self.__lock.acquire()
            self.__domain_dic[domain] = addrs
            sql = 'delete from web_domainip where domain="%s"' % domain
            self.__cursor.execute(sql)
            self.__conn.commit()
            for addr in addrs:
                sql = 'insert into web_domainip(first_domain, domain, ip, update_date) values("%s", "%s", "%s", now())' % (self.__father_domain, domain, addr)
                self.__cursor.execute(sql)
                self.__conn.commit()
            self.__lock.release()
        except dns.resolver.NoNameservers as e:
            print e.message
        except Exception, e:
            pass

    def percent(self):
        return self.__current_index


def new_domain_brute(domain_brute_id, domain, thread_num, model):
    domainBrute = DomainBrute(domain_brute_id, domain, thread_num=thread_num, option=model)
    domainBrute.load_dict()
    domainBrute.start()
    print 'domain end!'

# 没有递归爆破
if __name__ == '__main__':
    domain = 'runboo.com'
    domainBrute = DomainBrute(domain, thread_num=2)
    domainBrute.load_dict()
    domainBrute.start()
    print 'domain brute'