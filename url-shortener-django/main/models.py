from django.db import models
import datetime
# Create your models here.
class short_urls(models.Model):
    short_url = models.CharField(max_length=100)
    long_url = models.URLField("")
    expiry = models.DateTimeField(default=datetime.datetime.now, blank=False,null=True)