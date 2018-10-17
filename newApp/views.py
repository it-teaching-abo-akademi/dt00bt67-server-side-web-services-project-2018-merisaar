from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from .forms import BlogForm, CopyOfForm, UserCreationForm, CreateAuctionForm, EditAuctionForm
from .models import BlogModel, Auction

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
# Create your views here.

def hello(request):
    return HttpResponse("Hello world!")


def show_all_data(request):
    try:
        unexpired_posts = Auction.objects.filter(deadline__gt=datetime.now())

        # auctions = Auction.objects.order_by('-deadline')
    except Exception:
        return HttpResponse("Lopeta heti paikalla")
    return render(request, "homePage/show.html", {"auctions": unexpired_posts})

def bidAuction(request):
    HttpResponse("Implementing..")

class EditBlogView(View):
    def get(self, request, id):
        b = get_object_or_404(BlogModel, id=id)
        return render(request, "edit.html", {"blog": b})

    def post(self, request, id):
        # This will return an array of one blog or none
        blog = BlogModel.objects.get(id=id)
        form = BlogForm(request.POST, instance = blog)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Blog updated")
            return HttpResponseRedirect(reverse("home"))
        return HttpResponse('Error')


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

class Blog(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "forms.html", {"form": form})

    def post(self, request):
        form = BlogForm(request.POST)
        if(form.is_valid()):
            cd = form.cleaned_data
            blog_t = cd['title']
            blog_b = cd['body']
            form = CopyOfForm({"c_title": blog_t, "c_body": blog_b})
            return render(request, "confirmation.html", {"form": form})
            #Sessions:
            # request.session('blog_t') = blog_t
            # request.session('blog_b') = blog_b

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
            # token = default_token_generator.make_token(userAuction)
            # uid = urlsafe_base64_encode(force_bytes(userAuction.pk))
            messages.add_message(request, messages.INFO, "New auction created")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)
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
