from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Bookmark(models.Model):
    url = models.CharField(max_length=10000)
    # title = models.CharField(max_length=10000)
    # desc = models.CharField(max_length=10000)
    # iurl = models.CharField(max_length=10000)
    # author = models.CharField(max_length=10000)
    # pub_at = models.DateTimeField()
    username = models.CharField(max_length=10000)