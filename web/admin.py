from django.contrib.auth.models import User

import xadmin
from django.contrib import admin

# Register your models here.

'''
user:admin
password:Admin6666!
'''

# admin.site.register(User)
xadmin.site.register(User)