from django.db import models
from datetime import datetime,timedelta
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title