from ..forms import *
from ..models import Auction, BidAuction, Email
from ..decorators import superuser_required
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
from django.db import IntegrityError, OperationalError, transaction
from django.utils.translation import ugettext as _

@method_decorator(login_required, name='dispatch')
class BidAuctionClass(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user
            auction = get_object_or_404(Auction, id=id)
            highestBid = BidAuction.objects.filter(auction = auction).last()
            #Too many nested if statements
            request.session['description'] = auction.description
            if not highestBid:
                if (auction.seller == user):
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return render(request, "AuctionHandler/bidAuction.html", {"user": user, "auction": auction})
            else:
                if (highestBid.bidder == user) or auction.seller == user:
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return render(request, "AuctionHandler/bidAuction.html", {"user": user, "auction": auction})
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, id):
        auction = Auction.objects.get(id=id)
        form = BidAuctionForm(request.POST)
        if form.is_valid():
            #What about banned posts or already highest bids?
            cd = form.cleaned_data
            userBid = form.save(commit = False)
            userBid.bidder = request.user
            userBid.auction = auction
            value = cd['value']

            highestBid = BidAuction.objects.filter(auction = auction).last()
            passed = True
            saved = False
            if highestBid:
                if highestBid.bidder == userBid.bidder:
                    messages.add_message(self.request, messages.ERROR, "Already highest bid")
                    # raise ValidationError("User " + str(self.bidder) +" is already highest bidder.")
                    passed = False

            if userBid.auction.minimumPrice > value:
                passed = False
                # raise ValidationError("Can't bid less than highest bid.")
                messages.add_message(self.request, messages.INFO, "Can't bid less than highest bid")
            if userBid.auction.seller == userBid.bidder:
                passed = False
                # raise ValidationError("Can't bid to you own auction.")
                messages.add_message(self.request, messages.INFO, "Can't bid to you own auction")
            if 'description'in request.session:
                if not request.session.get('description') == userBid.auction.description:
                    passed = False
                    # raise ValidationError("Can't bid to you own auction.")
                    messages.add_message(self.request, messages.INFO, "Description has changed")

            if passed:
                try:
                    with transaction.atomic():
                        userBid.save()
                        saved = True
                except OperationalError:
                    messages.add_message(request, messages.ERROR, "Database locked. Try again.")
                    form = BidAuctionForm(request.POST)
                    return render(request, "AuctionHandler/bidAuction.html", {"user": request.user, "auction": auction})
            if saved:
                if highestBid:
                    send_mail('New bid on auction',
                    'New bid on auction titled ' + auction.auctionTitle + '.',
                    'merisrnn@gmail.com', [highestBid.bidder.email,])
                    mail = Email(title = 'New bid on auction',
                    body = 'New bid on auction you bidded on titled ' + auction.auctionTitle + '.',
                    emailTo = highestBid.bidder)
                    mail.save()
                    send_mail('New bid on you auction',
                    'New bid on your auction titled ' + auction.auctionTitle + '.',
                    'merisrnn@gmail.com', [auction.seller.email,])
                mail = Email(title = 'New bid on auction',
                body = 'New bid on your auction titled ' + auction.auctionTitle + '.',
                emailTo = auction.seller)
                mail.save()
                messages.add_message(request, messages.INFO, "Bid accepted")
                return HttpResponseRedirect(reverse("home"))
            else:
                form = BidAuctionForm(request.POST)
                return render(request, "AuctionHandler/bidAuction.html", {"user": request.user, "auction": auction})
        else:
            form = BidAuctionForm(request.POST)
            return render(request, "AuctionHandler/bidAuction.html", {"user": request.user, "auction": auction})

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
        saved = False
        try:
            with transaction.atomic():
                auction.save()
                saved = True
        except OperationalError:
            messages.add_message(request, messages.ERROR, "Database locked. Try again.")
            return render(request, "AuctionHandler/banAuction.html", {"auction": auction})

        if saved:
            #Send email to highestBidders and auction creator
            send_mail('Your auction has been banned',
             'Your auction titled ' + auction.auctionTitle + ' has been banned.',
             'merisrnn@gmail.com', [auction.seller.email,])
            mail = Email(title = 'Your auction has been banned',
                body = 'Your auction titled ' + auction.auctionTitle + ' has been banned.',
                emailTo = auction.seller)
            mail.save()
            list = BidAuction.objects.filter(auction = auction)
            if len(list)>0:
                massMailList = []
                for l in list:
                    massMailList.append(l.bidder.email)
                send_mail('Action you have bidded to has been banned',
                 'Auction titled ' + auction.auctionTitle + ' has been banned.',
                 'merisrnn@gmail.com', [massMailList])
                mail = Email(title = 'Action you have bidded to has been banned',
                    body = 'Auction titled ' + auction.auctionTitle + ' has been banned.',
                    emailTo = massMailList.objects.last())
                mail.save()
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
            saved = False
            try:
                with transaction.atomic():
                    form.save()
                    saved = True
            except OperationalError:
                messages.add_message(request, messages.ERROR, "Database locked. Try again.")
                return render(request, "AuctionHandler/editAuction.html", {"user": user, "auction": auction})
            if saved:
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
            cd = form.cleaned_data
            title = cd['auctionTitle']
            description = cd['description']
            minPrice = cd['minimumPrice']
            form = ConfAuctionForm({"title": title, "description": description, "minPrice": minPrice})
            return render(request, 'AuctionHandler/confirmation.html', {'form': form})

        else:
            messages.add_message(request, messages.ERROR, _("Not valid data"))
            return render(request, "AuctionHandler/auctionForm.html", {"form": form})

def saveAuction(request):
    option = request.POST.get('option', '')
    if option == 'Yes':
        title = request.POST.get('title', '')
        descr = request.POST.get('descr', '')
        minPrice = request.POST.get('minPrice', '')
        userAuction = Auction(auctionTitle = title, description= descr, minimumPrice=minPrice, seller = request.user)
        userAuction.save()
        messages.add_message(request, messages.INFO, _("New auction created"))
        send_mail('Auction added successfully.', 'Auction titled "' + userAuction.auctionTitle + '" added successfully. Description: "' + userAuction.description + '".', 'merisrnn@gmail.com', [userAuction.seller.email,])
        mail = Email(title = 'Auction added successfully.',
            body = 'Auction titled "' + userAuction.auctionTitle + '" added successfully. Description: "' + str(userAuction.description) + '".',
            emailTo = userAuction.seller)
        mail.save()
        # messages.add_message(request, messages.INFO, _("New blog has been saved"))
        return HttpResponseRedirect(reverse("home"))
    else:
        messages.add_message(request, messages.INFO, _("Auction cancelled"))
        return HttpResponseRedirect(reverse("home"))
