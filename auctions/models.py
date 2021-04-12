from django.contrib.auth.models import AbstractUser
from django.db import models

class Watchlists(models.Model):
    user=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mark=models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')


class User(AbstractUser):
    pass
class Auction_lists(models.Model):
    state=models.CharField(max_length=100)
    last_man=models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    price=models.FloatField()
    desc=models.CharField(max_length=800)
    image_url=models.CharField(max_length=8000000)
    category=models.CharField(max_length=20)
    class Meta:
        unique_together = ('user', 'name')

    pass
class Bids(models.Model):
    bid=models.FloatField()
    user=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
class Comments(models.Model):
    name=models.CharField(max_length=100)
    comment=models.CharField(max_length=1000)
    pass

