#!env/bin/python
# coding:utf-8

import socket
import threading
from multiprocessing.dummy import Pool as ThreadPool

import MySQLdb

from core.config import DB_CHARSET, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, INTERNET_TIMEOUT
from core.config import DB_HOST
from core.function import get_ip


class ScanPort:

    __target_ip = None
    __option = None
    __ports = {}
    __port_map = {}
    __thread_num = 1
    __percent = {}
    __lock = threading.Lock()
    __run = True
    __port_scan_id = 0
    __conn = None
    __cursor = None


    def __init__(self, port_scan_id=0, ipaddr=None, option="usually", thread_num=10):
        # if target_host is not None:
        #     self.__target_ip = get_ip(target_host)
        # IP 地址格式127.0.0.1
        # else:
        self.__target_ip = ipaddr
        self.__port_scan_id = port_scan_id
        self.__option = option
        self.__thread_num = thread_num
        socket.setdefaulttimeout(INTERNET_TIMEOUT)
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                               charset=DB_CHARSET)
        cursor = conn.cursor()
        sql = 'update web_portscan set status=1 where id=%d' % port_scan_id
        cursor.execute(sql)
        conn.commit()
        self.__cursor = cursor
        self.__conn = conn
        # cursor.close()
        # conn.close()

    def start(self):
        self.init_port_map()
        self.add_ports()
        pool = ThreadPool(processes=self.__thread_num)
        self.__pool = pool
        pool.map(self.scan_port, self.__ports)
        pool.close()
        pool.join()

    def scan_port(self, port):
        self.__lock.acquire()
        if self.__run is not True:
            pass
        self.__lock.release()
        try:
            s = socket.socket(2, 1)
            print 'port:', port
            res = s.connect_ex((self.__target_ip, port))
            if res == 0:  # 如果端口开启 发送 hello 获取banner
                try:
                    s.send('hello')
                    banner = s.recv(1024)
                except Exception as e:
                    print str(e.message)
                    self.__ports[port] = ''
                else:
                    self.__ports[port] = banner
                    print "open:", port, banner
            s.close()
        except Exception as e:
            # print str(e.message)
            pass
        self.__lock.acquire()
        self.__percent['current'] += 1
        if self.__percent['current'] % 10 == 0 or self.__percent['current'] >= self.__percent['all']:
            sql = 'update web_portscan set current_index=%d where id=%d' % (
            self.__percent['current'], self.__port_scan_id)
            self.__cursor.execute(sql)
            self.__conn.commit()
        self.__lock.release()

    def add_ports(self):
        # conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
        #                        charset=DB_CHARSET)
        # cursor = conn.cursor()
        if self.__option == 'all':
            for i in range(65534)[1:]:
                self.__ports[i] = 'close'
            self.__percent['all'] = i
            sql = 'update web_portscan set port_count=65534 where id=%d' % self.__port_scan_id
        elif self.__option == 'usually':
            count = 0
            for (num, name) in self.__port_map.items():
                self.__ports[num] = 'close'
                count += 1
            self.__percent['all'] = count
            sql = 'update web_portscan set port_count=%d where id=%d' % (count, self.__port_scan_id)
        self.__percent['current'] = 0
        self.__cursor.execute(sql)
        self.__conn.commit()
        # cursor.close()
        # conn.close()

    def init_port_map(self):
        self.__port_map[20] = 'FTP'
        self.__port_map[21] = 'FTP'
        self.__port_map[22] = 'SSH'
        self.__port_map[23] = 'Telnet'
        self.__port_map[25] = 'SMTP'
        self.__port_map[31] = 'MSG[木马]'
        self.__port_map[53] = 'DNS'
        self.__port_map[67] = 'DHCP Server'
        self.__port_map[68] = 'DHCP Client'
        self.__port_map[69] = 'Cisco TFTP'
        self.__port_map[79] = 'Finger'
        self.__port_map[80] = 'HTTP'
        self.__port_map[88] = 'Kerberos'
        self.__port_map[99] = 'Metagram Relay[ncx]'
        self.__port_map[102] = 'Message Transfer'
        self.__port_map[109] = 'POP2'
        self.__port_map[110] = 'POP3'
        self.__port_map[111] = 'SUN RPC'
        self.__port_map[113] = 'Windows Authentication Server'
        self.__port_map[119] = 'NNTP'
        self.__port_map[135] = 'RPC'
        self.__port_map[137] = 'NETBIOS'
        self.__port_map[138] = 'NETBIOS'
        self.__port_map[139] = 'NETBIOS/SMP'
        self.__port_map[143] = 'IMAP'
        self.__port_map[161] = 'SMTP'
        self.__port_map[162] = 'SNMP'
        self.__port_map[177] = 'Display Manager Control'
        self.__port_map[443] = 'HTTPS'
        self.__port_map[553] = 'CORBA IIOP[UDP RPC]'
        self.__port_map[554] = 'RTSP'
        self.__port_map[555] = 'DSF'
        self.__port_map[636] = 'LDAP'
        self.__port_map[666] = 'Doom Id software[backdoor]'
        self.__port_map[993] = 'IMAP SSL'
        self.__port_map[1024] = '网络访问起始地址'
        self.__port_map[1080] = 'SOCKETS'
        self.__port_map[1433] = 'SQL'
        self.__port_map[1500] = 'RPC'
        self.__port_map[1521] = 'Oracle'
        self.__port_map[1755] = 'MMS'
        self.__port_map[1999] = 'cisco'
        self.__port_map[2049] = 'NFS'
        self.__port_map[2504] = '网络负载均衡'
        self.__port_map[3306] = 'Mysql'
        self.__port_map[3389] = 'Remote Desktop'
        self.__port_map[7001] = 'WebLogic'
        self.__port_map[8000] = 'QICQ[QQ]'
        self.__port_map[8080] = 'www agency、 JBOSS、TOMCAT'
        self.__port_map[9080] = 'Websphere'

    def show_ports_information(self):
        for num, banner in self.__ports.items():
            if banner != 'close':
                show = '[PORT]:', num, 'is open'
                # show += "\t\t[banner]:", banner
                if num in self.__port_map.keys():
                    show += "\t\t[SERVER]:", self.__port_map[num]
                print show

    def get_percent(self):
        return self.__percent

    def stop(self):
        self.__pool.terminate()
        # for thread in self.__pool:
        #     thread.task_done()

    def submit_result(self):
        for num, banner in self.__ports.items():
            if banner != 'close':
                if num in self.__port_map.keys():
                    info = self.__port_map[num]
                sql = 'insert into web_openport(ip_addr, port_num, port_info) values("%s", %d, "%s")' % (self.__target_ip, num, info)
                self.__cursor.execute(sql)
        # 去掉了manytomany关联
        # sql = 'select id from web_openport where ip_addr="%s"' % self.__target_ip
        # self.__cursor.execute(sql)
        # openport_ids = self.__cursor.fetchall()
        # sql = 'select id from web_portscan where task_id_id=%d' % self.__task_id
        # self.__cursor.execute(sql)
        # portscan_id = self.__cursor.fetchone()
        # for openport_id in openport_ids:
        #     sql = 'insert into web_portscan_port_scan_result(portscan_id, openport_id) values(%d, %d)' % (portscan_id[0], openport_id[0])
        #     self.__cursor.execute(sql)
        # 设置完成状态2
        sql = 'update web_portscan set status=2 where id=%d' % self.__port_scan_id
        self.__cursor.execute(sql)
        self.__conn.commit()
        # 关闭数据库连接
        self.__cursor.close()
        self.__conn.close()


def new_port_scan(port_scan_id, ip, model, thread_num):
    # for ip in addrs:
    scanPort = ScanPort(port_scan_id=port_scan_id, ipaddr=ip, option=model, thread_num=thread_num)
    scanPort.start()
    scanPort.submit_result()
    # scanPort.show_ports_information()


if __name__ == '__main__':
    # scanPort = ScanPort(target_host="www.runoob.com", model="usually", thread_num=8)
    scanPort = ScanPort(ipaddr="113.105.245.122", option="usually", thread_num=8)
    scanPort.start()
    scanPort.show_ports_information()
