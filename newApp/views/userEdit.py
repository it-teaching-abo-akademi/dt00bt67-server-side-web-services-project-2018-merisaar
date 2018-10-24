from ..forms import *
from ..models import Auction, BidAuction
from ..decorators import superuser_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _
from django.urls import reverse

@method_decorator(login_required, name='dispatch')
class EditUser(TemplateView):
    def get(self, request):
        user = request.user
        auctions = Auction.objects.filter(seller = user)
        return render(request, "userView/userView.html", {"user": user, "auctions": auctions})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("home"))
        else: return HttpResponse('Error')

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data= request.POST, user= request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userView/change_password.html', {'form': form })

@login_required
def changeEmail(request):
    if request.method == 'POST':
        user =get_user_model().objects.filter(username=request.user.username)
        user.update(email=request.POST['email'])
        update_session_auth_hash(request, user)
        messages.success(request, _('Your email was successfully updated!'))
        return redirect('user_view')
        # else:
        #     messages.error(request, 'Please correct the error below.')
    else:
        return render(request, 'userView/base.html', {'user': request.user })
