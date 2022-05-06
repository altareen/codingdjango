#from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

#class User(AbstractUser):
#    pass

class Bid(models.Model):
    price = models.FloatField()
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchaser")

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="individual")
    category = models.CharField(max_length=64)
    timestamp = models.DateTimeField()
    url = models.TextField()
    bids = models.ManyToManyField(Bid, blank=True, related_name="listings")
    watchlist = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="listings")
    active = models.BooleanField(default=True)
    comments = models.ManyToManyField(Comment, blank=True, related_name="listings")
