#! env/bin/python
# coding:utf-8
import os
import subprocess

import MySQLdb

from tools.config import POC_PATH, DB_HOST, DB_CHARSET, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from tools.function import get_domain


class ProofAttack:

    __poc_files = None
    poc_name = ''
    __poc_path = POC_PATH
    __poc_set = []


    def __init__(self, target_host, cat, model):
        self.__target_host = target_host
        self.__cat = cat
        self.__poc_path = os.path.join(POC_PATH, model)

    def attack(self):
        pass

    def has_poc(self):
        path = os.path.join(self.__poc_path, self.__cat.lower())
        # for rt, dirs, files in os.walk(path):
        files = []
        try:
            for file in os.listdir(path):
                # print file
                files.append(path + os.sep + file)
        except Exception as e:
            print e
            self.__poc_files = None
            return False
        if not files:
            self.__poc_files = None
            return False
        else:
            self.__poc_files = files
            return True

    def proof(self, charset):
        if self.__poc_files is None:
            print'没有找到poc'
            return
        for file in self.__poc_files:
            if file in self.__poc_set:
                continue
            if file.split('\\')[-1] == '*.*':
                continue
            self.__poc_set.append(file)
            # result = os.popen('python ' + file)
            # charset = 'utf-8'
            p = subprocess.Popen('python ' + file + ' ' + self.__target_host, shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()
            # print 'output:'
            output = out.decode(charset)
            # print 'error:'
            error = str(err).decode(charset)
            if output.index(u"[SUCCESS]") != -1:
                file_name = file.split(os.sep)[-1]
                poc_name = file_name
                # poc_name = '.'.join(file_name.split('.')[:-1])
                self.poc_name = poc_name
                return '[success]'
            elif output.index(u'[PARAM]') != -1:
                return '[param]'
            else:
                return '[fails]'


def new_proof_attack(proof_id, url, model):
    try:
        domain = get_domain(url)
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        cursor = conn.cursor()
        if model == 'web':
            sql = 'select * from web_apptype WHERE domain="%s"' % domain
            cursor.execute(sql)
            apps = cursor.fetchall()
            for app_type in apps:
                proof_attack = ProofAttack(url, app_type[2], model)
                if proof_attack.has_poc():
                    result = proof_attack.proof(charset='utf-8')
                    if result == '[success]':
                        sql = 'insert into web_webproofresult(domain, result, poc_type, poc_name, update_date) values("%s", 1, "%s", "%s", now())' % (domain, app_type[2], proof_attack.poc_name)
                        cursor.execute(sql)
                        conn.commit()
            sql = 'update web_webproof set status=2'
            cursor.execute(sql)
            conn.commit()
        elif model == 'system':
            pass
        cursor.close()
        conn.close()
    except Exception as e:
        print e
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    proof_attack = ProofAttack('http://localhost/drupal-7.31/', 'drupal')
    if proof_attack.has_poc():
        proof_attack.proof()