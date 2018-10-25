from ..forms import *
from ..models import Auction, BidAuction
from ..decorators import superuser_required
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext as _

class AuctionList(ListView):
    queryset = Auction.objects.filter(banned = False, active=True)
    template_name = 'homePage/show.html'

@method_decorator([login_required, superuser_required], name='dispatch')
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
