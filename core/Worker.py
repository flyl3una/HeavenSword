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
from core.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET


def echo():
    pass


def start(params):
    conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    cursor = conn.cursor()
    thread_list = []
    task_id = params['task_id']
    if task_id is None:
        print 'task id error!!!'
        return
    # 指纹识别
    target_url = params['target']
    # if 'finger_flag' in params.keys():
    #     finger_thread = threading.Thread(target=get_finger, args=(task_id, target_url, ))
    #     thread_list.append(finger_thread)
    #     finger_thread.start()
    # 端口扫描
    # if 'port_scan_flag' in params.keys():
    #     if 'port_scan_thread' in params.keys():
    #         port_scan_thread_num = params['port_scan_thread']
    #     else:
    #         port_scan_thread_num = 4
    #     if 'port_scan_model' in params.keys():
    #         port_scan_model = str(params['port_scan_model'])
    #     else:
    #         port_scan_model = 'usually'
    #     port_scan_thread = threading.Thread(target=new_port_scan, args=(task_id, '113.105.245.122', port_scan_model, port_scan_thread_num, ))
    #     thread_list.append(port_scan_thread)
    #     port_scan_thread.start()
    # 二级域名爆破
    # if 'domain_brute_flag' in params.keys():
    #     if 'domain_brute_thread' in params.keys():
    #         domain_brute_thread = params['domain_brute_thread']
    #     else:
    #         domain_brute_thread = 4
    #     domain_brute_thread = threading.Thread(target=new_domain_brute, args=(task_id, 'runboo.com', domain_brute_thread))
    #     thread_list.append(domain_brute_thread)
    #     domain_brute_thread.start()

    # 网页爬虫
    # if 'spider_flag' in params.keys():
    #     if 'spider_thread' in params.keys():
    #         spider_thread = params['spider_thread']
    #     else:
    #         spider_thread = 4
    #     spider_thread = threading.Thread(target=new_spider, args=(task_id, target_url, spider_thread))
    #     thread_list.append(spider_thread)
    #     spider_thread.start()

    # 漏洞测试
    # if 'exploit_flag' in params.keys():
    #     exploit_thread = threading.Thread(target=new_exploit_attack, args=(task_id, target_url, 'drupal'))
    #     thread_list.append(exploit_thread)
    #     exploit_thread.start()

    for thread in thread_list:
        thread.join()

'''
python D:\work\pycharm\workspace\github\HeavenSword\core\worker.py {'task_id': 1, 'domain_brute_thread': 6, 'target': 'http://www.runoob.com', 'port_scan_thread': 4, 'spider_flag': true, 'port_scan_flag': true, 'domain_brute_flag': true, 'spider_thread': 8, 'exploit_flag': true, 'port_scan_model': 'usually', 'finger_flag': true}
'''

if __name__ == '__main__':
    # conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    # cursor = conn.cursor()
    # while True:
    #     pass
    json_args = ' '.join(sys.argv[1:])
    # opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    # for opt, value in opts:
    #     if opt == '-json':
    #         json_args = value
    #         args = json.loads(json_args)
    #         print args
    json_args = json_args.replace("'", '"')
    args = json.loads(json_args)
    print args
    start(args)
    # cursor.close()
    # conn.close()

