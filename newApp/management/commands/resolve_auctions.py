from django.core.management.base import BaseCommand, CommandError
from newApp.models import *
from django.utils import timezone
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Runs through email queue and sends emails'

    def add_arguments(self, parser):
        parser.add_argument('--id')

    def handle(self, *args, **options):
        if options['id']:
            self.send_email(email)
            email.delete()
        else:
            expiredList = Auction.objects.filter(deadline__lt = timezone.now(), active=True, banned=False)
            print(len(expiredList))
            for expired in expiredList:
                self.send_email(expired)
                expired.active = False
                expired.save()

    def send_email(self, expired):
        # try:
            bids = BidAuction.objects.filter(auction = expired)
            highestBid = bids.first()
            if highestBid:
                highestBid.hasWon = True
                highestBid.save()
                print('Your auction '+str(expired.auctionTitle) +  ' has expired. Winning bid was '+ str(expired.minimumPrice) + ' by user '  + str(highestBid.bidder))
                send_mail('Auction has expired',
                'Your auction ' + expired.auctionTitle + ' has expired. Winning bid was ' + str(expired.minimumPrice) + ' by user ' + str(highestBid.bidder.username) + ' ' +str(highestBid.bidder) + '.',
                'merisrnn@gmail.com', [expired.seller,])
                send_mail('Auction has expired, your bid won',
                'Auction ' + expired.auctionTitle + ' has expired. Your bid of ' + str(expired.minimumPrice) + ' has won! Contact seller using this email ' + str(expired.seller),
                'merisrnn@gmail.com', [highestBid.bidder,])
                list = BidAuction.objects.filter(auction = expired, hasWon = False)
                newList = []
                for bid in list:
                    print(bid.bidder.email)
                    newList.append(bid.bidder.email)
                send_mail('Action you have bidded to has expired',
                 'Auction titled ' + expired.auctionTitle + " has expired. Unfortunately your bid wasn't the winning bid.",
                 'merisrnn@gmail.com', [newList])
            else:
                print('Your auction '+str(expired.auctionTitle) +  ' has expired. There were no bids.')
                send_mail('Auction has expired',
                'Your auction ' + expired.auctionTitle + ' has expired. There were no bids.',
                'merisrnn@gmail.com', [expired.seller,])
        # except:
            # raise CommandError("Email could not send for reason XYZ")

    # def update_bid_row(self, bid):
    #     bid.email_sent = True
    #     bid.email_sent_time = timezone.now()
    #     bid.save()
