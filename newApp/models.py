from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime

# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

# class BlogModel(models.Model):
#     title = models.CharField(max_length=150)
#     timestamp = models.DateTimeField()
#     body = models.TextField()
#     def __str__(self):
#         return self.title

class Auction(models.Model):
    active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    auctionTitle = models.CharField(max_length=150)
    description = models.TextField()
    minimumPrice = models.DecimalField(max_digits=5, decimal_places=2)
    deadline = models.DateTimeField(default=datetime.now() + timedelta(hours=72))
    banned = models.BooleanField(default=False)

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
     value = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0)
     hasWon = models.BooleanField(default =False)

     # def save(self, *args, **kwargs):
     #    if BidAuction.objects.filter(auction = self.auction).first().bidder == self.bidder:
     #         print('Already highest bid')
     #    else:
     #        super(BidAuction, self).save(*args, **kwargs)


# class AuctionManager(models.Manager):
#     def active(self):
#         return super().get_queryset().filter(active=True)
#
#     def expired(self):
#         return super().get_queryset().filter(active=False)
#
# class EmailManager(models.Manager):
#     def emails(self):
#         return super().get_queryset().order_by('-created_at')
#
# class ProcessQueue(models.Model):
#     auction = models.ForeignKey(Auction, on_delete=None, blank=True, null=True)
#     bid = models.ForeignKey(BidAuction, on_delete=None, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     objects = models.Manager()
#     EmailManager = EmailManager()
