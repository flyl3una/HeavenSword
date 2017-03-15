#! env/bin/python
# coding:utf-8


def get_domain(url):
    url1 = url
    if url.find("//") != -1:
        url1 = url.split('//')[1]
    if url1.find('/') != -1:
        domain = url1.split('/')[0]
    else:
        domain = url1
    return domain


if __name__ == '__main__':
    url = 'http://www.runoob.com'
    domain = get_domain(url)
    print domain