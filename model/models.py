from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class SwordUser(models.Model):
    id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=32)
    mobile = models.IntegerField(max_length=12)

    status = models.IntegerField(max_length=1)

    class Mete:
        def __init__(self):
            pass
        unique_together = (("user", "status"),)

    def __unicode__(self):
        return self.user.username



