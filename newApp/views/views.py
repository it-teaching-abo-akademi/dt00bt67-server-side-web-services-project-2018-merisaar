from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from ..forms import *
from ..models import Auction, BidAuction
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
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from ..decorators import superuser_required


# def show_banned(request):
#     if request.user.is_superuser:
#         try:
#             banned_posts = Auction.objects.filter(banned = True)
#             auctions = banned_posts.order_by('-deadline')
#         except Exception:
#             return HttpResponse("Lopeta heti paikalla")
#         return render(request, "homePage/show.html", {"auctions":auctions})
#     else:
#         unexpired_posts = Auction.objects.filter(deadline__gt=datetime.now(), banned = False)
#         return render(request, "homePage/show.html", {"auctions": unexpired_posts})


class registerUser(View):
    def get(self, request):
        form= UserCreationForm()
        return render(request, "registration/registration.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.INFO, "New user created")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)

            return render(request, "registration/registration.html", {"form": form})
