from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime

# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

class BlogModel(models.Model):
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    body = models.TextField()
    def __str__(self):
        return self.title

class Auction(models.Model):
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    # state = models.ForeignKey(
    #     State, on_delete=models.CASCADE
    # )
    auctionTitle = models.CharField(max_length=150)
    description = models.TextField()
    minimumPrice = models.DecimalField(max_digits=5, decimal_places=2)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(hours=72))
    banned = models.BooleanField(default=False)

    def __str__(self):
         return "{} {}".format(self.auctionTitle, self.description)
# class State(models.Model):
#     active = models.BooleanField(default=True)
#     banned = models.BooleanField(default=False)
#     due = models.BooleanField(default=False)
#     adjudicated = models.BooleanField(default=False)

class BidAuction(models.Model):
     bidder = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
     )
     timestamp = models.DateTimeField(default=datetime.now())
     auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, null = True, related_name = "bidder"
     )
     bid = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)
