#!env/bin/python
# coding:utf-8

import socket
from multiprocessing.dummy import Pool as ThreadPool


class ScanPort:

    __target_ip = None
    __model = None
    __ports = {}
    __port_map = {}
    __thread_num = 1


    def __init__(self, target_host=None, ipaddr=None, model="usually", thread_num=1):
        if target_host is not None:
            self.__target_ip = socket.gethostbyname(target_host)
        #IP 地址格式127.0.0.1
        else:
            self.__target_ip = ipaddr
        self.__model = model
        self.__thread_num = thread_num
        socket.setdefaulttimeout(0.5)

    def start(self):
        self.init_port_map()
        self.add_ports()
        pool = ThreadPool(processes=self.__thread_num)
        pool.map(self.scan_port, self.__ports)
        pool.close()
        pool.join()

    def scan_port(self, port):
        try:
            s = socket.socket(2, 1)
            res = s.connect_ex((self.__target_ip, port))
            if res == 0:  # 如果端口开启 发送 hello 获取banner
                try:
                    s.send('hello')
                    banner = s.recv(1024)
                except Exception, e:
                    print str(e.message)
                    self.__ports[port] = ''
                else:
                    self.__ports[port] = banner

            s.close()
        except Exception, e:
            print str(e.message)

    def add_ports(self):
        if self.__model == 'all':
            for i in range(65534)[1:]:
                self.__ports[i] = 'close'
        elif self.__model == 'usually':
            for (num, name) in self.__port_map.items():
                self.__ports[num] = 'close'

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


if __name__ == '__main__':
    # scanPort = ScanPort(target_host="www.runoob.com", model="usually", thread_num=8)
    scanPort = ScanPort(ipaddr="113.105.245.122", model="usually", thread_num=8)
    scanPort.start()
    scanPort.show_ports_information()
