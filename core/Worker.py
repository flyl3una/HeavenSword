#!env/bin/python
#coding:utf-8
import getopt
import json
import threading

import MySQLdb

# def listen_db():
import sys

from DomainBrute import new_domain_brute
from Exploit_attack import new_exploit_attack
from Finger import get_finger
from PortScan import new_port_scan
from Spider import new_spider
from core.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET, FINGER_PATH
from core.function import get_domain, get_first_domain


def echo():
    pass


def start_single_task(params):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        cursor = conn.cursor()
        thread_list = []
        # task_id = params['task_id']
        # if task_id is None:
        #     print 'task id error!!!'
        #     return

        # target_url = params['target']
        finger_thread = None
        # 指纹识别
        if 'finger_flag' in params.keys() and params['finger_flag']:
            finger_thread = threading.Thread(target=get_finger, args=(params['finger_id'], params['finger_target_url']))
            thread_list.append(finger_thread)
            # finger_thread.start()

        # 端口扫描
        if 'port_scan_flag' in params.keys() and params['port_scan_flag']:
            if 'port_scan_thread' in params.keys():
                port_scan_thread_num = params['port_scan_thread']
            else:
                port_scan_thread_num = 4
            if 'port_scan_model' in params.keys():
                port_scan_model = str(params['port_scan_model'])
            else:
                port_scan_model = 'usually'
            port_addr2id = params['port_addr2id']
            for ip, id in port_addr2id.items():
                port_scan_thread = threading.Thread(target=new_port_scan, args=(id, ip, port_scan_model, port_scan_thread_num))
                thread_list.append(port_scan_thread)
                # port_scan_thread.start()
            # addrs = args['port_addrs']
            # for ip in addrs:
            #     port_scan_thread = threading.Thread(target=new_port_scan, args=(task_id, ip, port_scan_model, port_scan_thread_num))
            #     thread_list.append(port_scan_thread)
            #     port_scan_thread.start()

        # 二级域名爆破
        if 'domain_brute_flag' in params.keys() and params['domain_brute_flag']:
            if 'domain_brute_thread' in params.keys():
                domain_brute_thread = params['domain_brute_thread']
            else:
                domain_brute_thread = 4
            first_domain = params['target_first_domain']
            domain_brute_id = params['domain_brute_id']
            # domain = get_domain(target_url)
            # domain = get_first_domain(domain)
            if first_domain:
                domain_brute_thread = threading.Thread(target=new_domain_brute, args=(domain_brute_id, first_domain, domain_brute_thread))
                thread_list.append(domain_brute_thread)
                # domain_brute_thread.start()

        # 网页爬虫
        if 'spider_flag' in params.keys() and params['spider_flag']:
            if 'spider_thread' in params.keys():
                spider_thread = params['spider_thread']
            else:
                spider_thread = 4
            target_url = params['target_url']
            url_list = target_url.split('/')[:3]
            url = url_list[0] + "//" + url_list[2]
            spider_id = params['spider_id']
            spider_thread = threading.Thread(target=new_spider, args=(spider_id, url, spider_thread))
            thread_list.append(spider_thread)
            # spider_thread.start()

        # 漏洞测试
        # 最后一布，放后面完成
        if 'exploit_flag' in params.keys() and params['exploit_flag']:
            target = args['exploit_url']
            url = '/'.join(target.split('/')[:3])
            exploit_id = args['exploit_id']
            exploit_thread = threading.Thread(target=new_exploit_attack, args=(exploit_id, url))
            # thread_list.append(exploit_thread)
            # exploit_thread.start()
        #
        for thread in thread_list:
            thread.start()
        if finger_thread:
            finger_thread.join()
        exploit_thread.start()
        thread_list.append(exploit_thread)
        for thread in thread_list:
            thread.join()
        sql = 'update web_singletask set task_status=1 where id="%d"' % params['task_id']
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print e
        for thread in thread_list:
            thread.join()
        print


def start_auto_task(params):
    target = params['target']
    task_id = params['task_id']
    # get_finger1(target)

'''
python D:\study\python\pycharm\workspace\HeavenSword\core\worker.py {'domain_brute_id': 2, 'exploit_url': 'http://drupal.xxx.com', 'domain_brute_thread': 10, 'target': 'http://drupal.xxx.com/', 'port_scan_thread': 10, 'target_first_domain': 'xxx.com', 'spider_flag': false, 'exploit_id': 1, 'port_addr2id': {'127.0.0.1': 2}, 'port_scan_model': 'usually', 'port_scan_flag': true, 'domain_brute_flag': true, 'port_addrs': ['127.0.0.1'], 'exploit_flag': true, 'finger_id': 2, 'task_id': 4, 'finger_target_url': 'http://drupal.xxx.com/', 'finger_flag': true}

python D:\study\python\pycharm\workspace\HeavenSword\core\worker.py {'exploit_url': 'http://drupal.xxx.com', 'target': 'http://drupal.xxx.com', 'task_id': 7, 'exploit_id': 4, 'exploit_flag': true, 'finger_id': 4, 'finger_target_url': 'http://drupal.xxx.com', 'finger_flag': true}
'''

if __name__ == '__main__':
    # conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    # cursor = conn.cursor()
    # while True:
    #     pass

    json_args = ' '.join(sys.argv[1:])
    json_args = json_args.replace("'", '"')
    args = json.loads(json_args)
    print args
    start_single_task(args)

    # cursor.close()
    # conn.close()

