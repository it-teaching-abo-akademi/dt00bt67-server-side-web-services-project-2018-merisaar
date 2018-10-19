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
from newApp.views import *
import django.contrib.auth.views
# from newApp.models import BlogModel

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'home/'}, name='logout'),
    path('hello/', hello),
    path('home/', show_all_data, name ="home"),
    # path('edit/<int:id>/', EditBlogView.as_view(), name="edit_blog"),
    # path('add/', Blog.as_view()),
    # path('saveAuction/', saveAuction, name = "save_form"),
    path('register/', registerUser.as_view(),  name = "register_user"),
    path('user/', EditUser.as_view(), name = "user_view"),
    path('user/password/', changePassword, name = "change_password"),
    path('user/email/', changeEmail, name = "change_email"),
    path('home/auction', AddAuction.as_view() , name = "add_auction"),
    path('home/auction/bid/<int:id>/', BidAuctionClass.as_view() , name = "bid_auction"),
    path('home/auction/edit/<int:id>/', EditAuction.as_view() , name = "edit_auction"),
    path('home/auction/ban/<int:id>/', BanAuction.as_view() , name = "ban_auction"),
    path('home/auction/banned/', show_banned , name = "banned_auctions"),

    ]
