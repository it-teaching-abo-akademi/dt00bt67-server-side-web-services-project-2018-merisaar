"""newProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url
from newApp.views.auctionHandling import *
from newApp.views.home import *
from newApp.views.userEdit import *
from newApp.views.general import *
import django.contrib.auth.views
from django.conf.urls import include
from newApp.restframework_rest_api import *
# from newApp.models import BlogModel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'home/'}, name='logout'),
    path('home/', AuctionList.as_view(), name ="home"),
    path('register/', registerUser.as_view(),  name = "register_user"),
    path('user/', EditUser.as_view(), name = "user_view"),
    path('user/password/', changePassword, name = "change_password"),
    path('user/email/', changeEmail, name = "change_email"),
    path('auction', AddAuction.as_view() , name = "add_auction"),
    path('auction/bid/<int:id>/', BidAuctionClass.as_view() , name = "bid_auction"),
    path('auction/edit/<int:id>/', EditAuction.as_view() , name = "edit_auction"),
    path('auction/ban/<int:id>/', BanAuction.as_view() , name = "ban_auction"),
    path('auction/banned/', AuctionBannedList.as_view() , name = "banned_auctions"),
    path('auction/search', SearchList.as_view() , name = "search_list_view"),
    path('auction/banned/search', SearchBannedList.as_view() , name = "search_banned_list"),
    path('language/', change_language, name="change_language"),
    path('currency/', currencyExhange, name="currency_convert"),
    path('api/auctions/', auction_list),
    path('api/auctions/<int:pk>/', AuctionDetail.as_view()),
    path('api/auctions/<slug:searchString>', AuctionDetailSearch.as_view()),
    path('api/auctions/<int:id>/bid', AuctionBidding.as_view()),
    ]
