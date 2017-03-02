#!env/bin/python
#coding:utf-8
import MySQLdb


# def listen_db():



if __name__ == '__main__':
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='wikipedia', charset='utf8')
    cursor = conn.cursor()
    while True:
        pass
