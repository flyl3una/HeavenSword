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
from tools.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET, FINGER_PATH
from tools.function import get_domain, get_first_domain


def start_single_web_task(params):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        cursor = conn.cursor()

        # 指纹识别
        if params['finger_flag']:
            # finger_thread = threading.Thread(target=get_finger, args=(params['finger_id'], params['finger_target_url']))
            # finger_thread.start()
            finger_id = params['finger_id']
            target_url = params['finger_target_url']
            get_finger(finger_id, target_url)

        # 漏洞测试
        # 最后一布，放后面完成
        if params['exploit_flag']:
            target = args['exploit_url']
            url = target
            exploit_id = args['exploit_id']
            # exploit_thread = threading.Thread(target=new_exploit_attack, args=(exploit_id, url))
            new_exploit_attack(exploit_id, url, 'web')

        sql = 'update web_websingletask set status=1 where id="%d"' % params['task_id']
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print e


def start_port_scan(params):
    # conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    # cursor = conn.cursor()
    if 'port_scan_thread' in params.keys():
        port_scan_thread_num = params['port_scan_thread']
    else:
        port_scan_thread_num = 4
    if 'port_scan_model' in params.keys():
        port_scan_model = str(params['port_scan_model'])
    else:
        port_scan_model = 'usually'
    id = params['port_scan_id']
    ip = params['ip']
    port_scan_thread = threading.Thread(target=new_port_scan, args=(id, ip, port_scan_model, port_scan_thread_num))
    # sql = 'update web_portscan set status=1 where id="%d"' % id
    # cursor.execute(sql)
    # conn.commit()
    # cursor.close()
    # conn.close()
    port_scan_thread.start()
    port_scan_thread.join()
    return True


def start_domain_brute(params):
    # 二级域名爆破
    if 'domain_brute_thread' in params.keys():
        domain_brute_thread_num = params['domain_brute_thread']
    else:
        domain_brute_thread_num = 4
    first_domain = params['first_domain']
    domain_brute_id = params['domain_brute_id']
    model = params['domain_brute_model']
    if not first_domain:
        return False
    domain_brute_thread = threading.Thread(target=new_domain_brute, args=(domain_brute_id, first_domain, domain_brute_thread_num, model))
    # conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
    # cursor = conn.cursor()
    # sql = 'update web_domainbrute set status=1 where id="%d"' % domain_brute_id
    # cursor.execute(sql)
    # conn.commit()
    # cursor.close()
    # conn.close()
    domain_brute_thread.start()
    domain_brute_thread.join()
    return True


def start_spider(params):
    # 网页爬虫
    if 'spider_thread' in params.keys():
        spider_thread = params['spider_thread']
    else:
        spider_thread = 4
    target_url = params['target_url']
    # domain = params['domain']
    url_list = target_url.split('/')[:3]
    url = url_list[0] + "//" + url_list[2]
    spider_id = params['spider_id']
    spider_thread = threading.Thread(target=new_spider, args=(spider_id, url, spider_thread))
    spider_thread.start()
    spider_thread.join()

'''
'''

if __name__ == '__main__':
    json_args = ' '.join(sys.argv[1:])
    json_args = json_args.replace("'", '"')
    args = json.loads(json_args)
    # print args
    model = args['model']
    if model == 1:
        #单个web任务
        start_single_web_task(args)
    elif model == 11:
        #端口扫描
        start_port_scan(args)
    elif model == 12:
        start_domain_brute(args)
    elif model == 13:
        #web爬虫
        start_spider(args)

