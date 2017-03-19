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


'''

'''

if __name__ == '__main__':
    json_args = ' '.join(sys.argv[1:])
    json_args = json_args.replace("'", '"')
    args = json.loads(json_args)
    print args
    model = args['model']
    if model == 1:
        #单个web任务
        start_single_web_task(args)


