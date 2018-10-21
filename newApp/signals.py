# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import *
#
#
# @receiver(post_save, sender=BidAuction)
# def update_auction_totals_for_bid(sender, instance, created, **kwargs):
#     if created:
#         print('In signal.py')
#         auction = instance.auction
#         auction.bid_count = Bid.BidManager.current(auction).count()
#         auction.current_bid = instance.value
#         auction.save()
