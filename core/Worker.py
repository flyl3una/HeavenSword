#!env/bin/python
#coding:utf-8
import getopt
import json

import MySQLdb

# def listen_db():
import sys

from core.Finger import get_finger
from core.PortScan import new_port_scan


def echo():
    pass


def start(params):
    target = params['target']
    if 'finger_flag' in params.keys():
        finger_ret = get_finger(target)
        print finger_ret
    if 'port_scan_flag' in params.keys():
        pass
        # if 'port_scan_thread' in params.keys():
        #     m_port_scan.port_scan_thread = params['port_scan_thread']
        # if 'port_scan_model' in params.keys():
        #     m_port_scan.port_scan_model = params['port_scan_model']
        new_port_scan(ip='113.105.245.122', model=str(params['port_scan_model']), thread_num=params['port_scan_thread'])
    if 'domain_brute_flag' in params.keys():
        pass
        
    #     if 'domain_brute_thread' in params.keys():
    #         domain_brute.domain_brute_thread = params['domain_brute_thread']
    if 'spider_flag' in params.keys():
        pass
    #     if 'spider_thread' in params.keys():
    #         m_spider.spider_thread = params['spider_thread']
    if 'exploit_attack_flag' in params.keys():
        pass
        # m_exploit_attack = models.ExploitAttack(target_domain=target, task_id=m_single_task)


if __name__ == '__main__':
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='HeavenSword', charset='utf8')
    cursor = conn.cursor()
    # while True:
    #     pass
    json_args = str(sys.argv[1:])
    # opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    # for opt, value in opts:
    #     if opt == '-json':
    #         json_args = value
    #         args = json.loads(json_args)
    #         print args
    args = json.loads(json_args)
    print args
    start(args)
    cursor.close()
    conn.close()

