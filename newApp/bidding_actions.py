# from .models import ProcessQueue
#
# class BiddingActions():
#
#     auction = None
#
#     def __init__(self, instance):
#         self.auction = instance
#
#     def update_auction(self):
#         auction = self.auction
#         # auction.bid_count = BidAuction.BidManager.current(auction).count()
#         auction.minimumPrice = format(auction.value, ".2f")
#         auction.save()
#
#     def send_email(self):
#         ProcessQueue(auction=self.auction).save()
