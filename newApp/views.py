from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from .forms import *
from .models import Auction, BidAuction

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from django.core.mail import send_mail
from functools import reduce
import operator
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.

def show_all_data(request):
    try:
        unexpired_posts = Auction.objects.filter(banned = False, active=True)
        auctions = unexpired_posts.order_by('-deadline')
        # auctions = Auction.objects.order_by('-deadline')
    except Exception:
        return HttpResponse("Lopeta heti paikalla")
    return render(request, "newApp/auction_list.html", {"auctions": auctions})

class AuctionList(ListView):
    queryset = Auction.objects.filter(banned = False, active=True).order_by('-deadline')
    template_name = 'homePage/show.html'

class AuctionBannedList(ListView):
    queryset = Auction.objects.filter(banned = True).order_by('-deadline')
    template_name = 'bannedList/banned_list.html'

class SearchList(ListView):
    paginate_by = 10
    template_name = 'homePage/show.html'
    def get_queryset(self):
        result = Auction.objects.filter(banned = False, active=True)
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(auctionTitle__icontains=query)
                # reduce(operator.and_,
                #        (Q(auctionTitle__icontains=q) for q in query_list))
            # )

        return result
class SearchBannedList(ListView):
    paginate_by = 10
    template_name = 'bannedList/banned_list.html'
    def get_queryset(self):
        result = Auction.objects.filter(banned = True)
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(auctionTitle__icontains=query)
                # reduce(operator.and_,
                #        (Q(auctionTitle__icontains=q) for q in query_list))
            # )

        return result

def show_banned(request):
    if request.user.is_superuser:
        try:
            banned_posts = Auction.objects.filter(banned = True)
            auctions = banned_posts.order_by('-deadline')
        except Exception:
            return HttpResponse("Lopeta heti paikalla")
        return render(request, "homePage/show.html", {"auctions":auctions})
    else:
        unexpired_posts = Auction.objects.filter(deadline__gt=datetime.now(), banned = False)
        return render(request, "homePage/show.html", {"auctions": unexpired_posts})

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
            highestBid = BidAuction.objects.filter(auction = auction).first()
            userBid = form.save(commit = False)
            userBid.bidder = request.user
            userBid.auction = auction
            auction.minimumPrice = userBid.value
            #Soft deadline
            # if(userBid.deadline<datetime.now()+timedelta(minutes=5) && userBid.deadline> datetime.now()):
            #     userBid.deadline= datetime.now()+timedelta(minutes=5)
            userBid.save()

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
        send_mass_mail('Action you have bidded to has been banned',
         'Auction titled ' + auction.auctionTitle + ' has been banned.',
         'merisrnn@gmail.com', [list])

        messages.add_message(request, messages.INFO, "Auction banned")
        return HttpResponseRedirect(reverse("home"))

class EditAuction(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user
            auction = get_object_or_404(Auction, id=id)
            if (auction.seller == user):
                return render(request, "AuctionHandler/editAuction.html", {"user": user, "auction": auction})
            else:
                return render(reverse("home"))
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request, id):
        auction = Auction.objects.get(id=id)
        form = EditAuctionForm(request.POST, instance = auction)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Auction description updated")
            return HttpResponseRedirect(reverse("home"))
        return HttpResponse(auction)


class EditUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            auctions = Auction.objects.filter(seller = user)
            return render(request, "userView/userView.html", {"user": user, "auctions": auctions})
        else:
            return HttpResponseRedirect(reverse("login"))

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("home"))
        else: return HttpResponse('Error')

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data= request.POST, user= request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userView/change_password.html', {'form': form })

def changeEmail(request):
    if request.method == 'POST':
        user =get_user_model().objects.filter(username=request.user.username)
        user.update(email=request.POST['email'])
        update_session_auth_hash(request, user)
        messages.success(request, 'Your email was successfully updated!')
        return redirect('user_view')
        # else:
        #     messages.error(request, 'Please correct the error below.')
    else:
        return render(request, 'userView/base.html', {'user': request.user })


def createAuction(request):
    if request.user.is_authenticated:
        return HttpResponse('In progress.')
    else:
        return HttpResponse('You have to logged in to view this page.')


class AddAuction(View):
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
            messages.add_message(request, messages.INFO, "New auction created")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = CreateAuctionForm(request.POST)
            return render(request, "AuctionHandler/auctionForm.html", {"form": form})

# def saveAuction(request):
#     option = request.POST.get('option', 'no')
#     if option == 'yes':
#         title = request.POST.get('c_title', '')
#         body = request.POST.get('c_body', '')
#         blog = BlogModel(title=title, timestamp=datetime.datetime.now(), body=body)
#         blog.save()
#         return HttpResponseRedirect(reverse("home"))
#     else:
#         messages.add_message(request, messages.INFO, "Whatever")
#         return HttpResponseRedirect(reverse("save_form"))


class registerUser(View):
    def get(self, request):
        form= UserCreationForm()

        return render(request, "registration/registration.html", {"form": form})


    def post(self, request):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):

            form.save()
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.clean_password2['password']
            # new_user = User(username= username,email= email, password = password, timestamp = datetime.datetime.now())
            # new_user.save()

            messages.add_message(request, messages.INFO, "New user created")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)

            return render(request, "registration/registration.html", {"form": form})

            # class Blog(View):
            #     def get(self, request):
            #         form = BlogForm()
            #         return render(request, "forms.html", {"form": form})
            #
            #     def post(self, request):
            #         form = BlogForm(request.POST)
            #         if(form.is_valid()):
            #             cd = form.cleaned_data
            #             blog_t = cd['title']
            #             blog_b = cd['body']
            #             form = CopyOfForm({"c_title": blog_t, "c_body": blog_b})
            #             return render(request, "confirmation.html", {"form": form})
            #             #Sessions:
            #             # request.session('blog_t') = blog_t
            #             # request.session('blog_b') = blog_b
