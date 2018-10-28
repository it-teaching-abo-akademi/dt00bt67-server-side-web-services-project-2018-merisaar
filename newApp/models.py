from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    # language = models.SlugField(max_length=100, default='en')
    language = models.CharField(max_length=10,
                                    choices=settings.LANGUAGES,
                                    default=settings.LANGUAGE_CODE)
    def __str__(self):
        return self.email

class Auction(models.Model):
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    auctionTitle = models.CharField(max_length=150)
    description = models.TextField()
    minimumPrice = models.DecimalField(max_digits=8, decimal_places=2)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(hours=72))
    banned = models.BooleanField(default=False)
    class Meta:
        ordering = ['-deadline']

    def __str__(self):
         return "{} {}".format(self.auctionTitle, self.description)

class BidAuction(models.Model):
    bidder = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(
    Auction, on_delete=models.CASCADE, null = True, related_name = "auctionBid"
    )
    value = models.DecimalField(max_digits=8, decimal_places=2, default = 0.0)
    hasWon = models.BooleanField(default =False)


class Email(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    emailTo = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null = True, related_name = "emailTo"
    )
    body = models.TextField()
    title = models.CharField(max_length=150)
