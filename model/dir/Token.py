#!env/bin/python
# coding: utf-8

from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re


class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)


if __name__ == '__main__':
    y = 0
    x = 100000
    i = 0
    while y < (5000.0/0.87):
        z = x*0.0005
        y += z
        x -=z
        i += 1
    print i, x, y