from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from ..forms import *
from ..models import Auction, BidAuction, Email
from django.core.mail import send_mail
from django.utils import translation
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
import requests
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import superuser_required

def change_language(request):
    lang_code =request.POST['language']
    user =get_user_model().objects.filter(username=request.user.username)
    user.update(language=lang_code)
    update_session_auth_hash(request, user)
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    messages.add_message(request, messages.INFO, _("Language Changed to ") + lang_code)
    return HttpResponseRedirect(reverse("user_view"))

def currencyExhange(request):
    cFrom = 'EUR'
    cTo = request.POST['currency']
    response = requests.get("https://free.currencyconverterapi.com/api/v6/convert?q=" + cFrom + "_" + cTo + "&compact=y")
    data = response.json()
    if(data):
        convertionRate = data[cFrom + '_' + cTo]['val']
        request.session['convRate'] = convertionRate
        request.session['currency'] = cTo
        return HttpResponseRedirect(reverse("home"))
    return HttpResponseRedirect(reverse("home"))

@method_decorator([login_required, superuser_required], name='dispatch')
class EmailList(ListView):
    queryset = Email.objects.all()
    template_name = 'emailhistory.html'

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
