from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from ..forms import *
from ..models import Auction, BidAuction
from django.core.mail import send_mail
from django.utils import translation
from django.utils.translation import ugettext as _
from django.urls import reverse

def change_language(request, lang_code):
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    messages.add_message(request, messages.INFO, _("Language Changed to ") + lang_code)
    return HttpResponseRedirect(reverse("home"))


class registerUser(View):
    def get(self, request):
        form= UserCreationForm()
        return render(request, "registration/registration.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.add_message(request, messages.INFO, _("New user created"))
            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)

            return render(request, "registration/registration.html", {"form": form})
