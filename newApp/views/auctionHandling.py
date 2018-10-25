from ..forms import *
from ..models import Auction, BidAuction
from ..decorators import superuser_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _

@method_decorator(login_required, name='dispatch')
class BidAuctionClass(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user
            auction = get_object_or_404(Auction, id=id)
            highestBid = BidAuction.objects.filter(auction = auction).first()
            #Too many nested if statements
            if not highestBid:
                if (auction.seller == user):
                    return render(request, "AuctionHandler/editAuction.html", {"user": user, "auction": auction})
                else:
                    return render(request, "AuctionHandler/bidAuction.html", {"user": user, "auction": auction})
            else:
                if (highestBid.bidder == user):
                    return HttpResponseRedirect(reverse("home"))
                elif auction.seller == user:
                    return render(request, "AuctionHandler/editAuction.html", {"user": user, "auction": auction})
                else:
                    return render(request, "AuctionHandler/bidAuction.html", {"user": user, "auction": auction})
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, id):
        auction = Auction.objects.get(id=id)
        form = BidAuctionForm(request.POST)
        if form.is_valid():
            #What about banned posts or already highest bids?
            userBid = form.save(commit = False)
            userBid.bidder = request.user
            userBid.auction = auction
            #Soft deadline
            # if(userBid.deadline<datetime.now()+timedelta(minutes=5) && userBid.deadline> datetime.now()):
            #     userBid.deadline= datetime.now()+timedelta(minutes=5)
            userBid.save()
            highestBid = BidAuction.objects.filter(auction = auction).first()

            if highestBid:
                send_mail('New bid on auction',
                'New bid on your auction titled ' + auction.auctionTitle + '.',
                'merisrnn@gmail.com', [highestBid.bidder.email,])
            send_mail('New bid on you auction',
            'New bid on your auction titled ' + auction.auctionTitle + '.',
             'merisrnn@gmail.com', [auction.seller.email,])
            messages.add_message(request, messages.INFO, "Bid accepted")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = BidAuctionForm(request.POST)
            return render(request, "AuctionHandler/auctionForm.html", {"form": form})

#Gets form for banning auction and sets auction to banned
@method_decorator([login_required, superuser_required], name='dispatch')
class BanAuction(View):
    def get(self, request, id):
        if request.user.is_superuser:
            user = request.user
            auction = get_object_or_404(Auction, id=id)
            return render(request, "AuctionHandler/banAuction.html", {"auction": auction})

    def post(self, request, id):
        auction = Auction.objects.get(id=id)
        auction.banned = True
        auction.active = False
        auction.save()
        #Send email to highestBidders and auction creator
        send_mail('Your auction has been banned',
         'Your auction titled ' + auction.auctionTitle + ' has been banned.',
         'merisrnn@gmail.com', [auction.seller.email,])
        list = BidAuction.objects.filter(auction = auction)
        massMailList = []
        for l in list:
            massMailList.append(l.bidder.email)
        send_mail('Action you have bidded to has been banned',
         'Auction titled ' + auction.auctionTitle + ' has been banned.',
         'merisrnn@gmail.com', [massMailList])

        messages.add_message(request, messages.INFO, _("Auction banned"))
        return HttpResponseRedirect(reverse("home"))

@method_decorator(login_required, name='dispatch')
class EditAuction(TemplateView):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user
            auction = get_object_or_404(Auction, id=id)
            if (auction.seller == user):
                return render(request, "AuctionHandler/editAuction.html", {"user": user, "auction": auction})
            else:
                return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, id):
        auction = Auction.objects.get(id=id)
        form = EditAuctionForm(request.POST, instance = auction)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _("Auction description updated"))
            return HttpResponseRedirect(reverse("home"))
        return HttpResponse(auction)


@method_decorator(login_required, name='dispatch')
class AddAuction(TemplateView):
    def get(self, request):
        form = CreateAuctionForm()
        return render(request, "AuctionHandler/auctionForm.html", {"form": form})

    def post(self, request):
        form = CreateAuctionForm(request.POST)
        if(form.is_valid()):
            userAuction = form.save(commit = False)
            userAuction.seller = request.user
            userAuction.save()
            send_mail('Auction added successfully.', 'Auction titled "' + userAuction.auctionTitle + '" added successfully. Description: "' + userAuction.description + '".', 'merisrnn@gmail.com', [userAuction.seller.email,])
            messages.add_message(request, messages.INFO, _("New auction created"))
            return HttpResponseRedirect(reverse("home"))
        else:
            form = CreateAuctionForm(request.POST)
            return render(request, "AuctionHandler/auctionForm.html", {"form": form})
