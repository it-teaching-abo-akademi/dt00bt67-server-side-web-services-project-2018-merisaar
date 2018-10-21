from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

class AuctionAdmin(admin.ModelAdmin):
    list_display = ['auctionTitle', 'minimumPrice', 'deadline', 'active']

    def current_bid_display(self, obj):
        return "£{0}".format(obj.highestBid)


class BidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'value', 'bidder', 'timestamp', 'hasWon']
    list_filter = (
        ('auction',)
    )

# class EmailAdmin(admin.ModelAdmin):
#     list_display = ['auction', 'bid', 'created_at']
#     list_filter = (
#         ('auction',)
#     )
#
#     def email_to(self, obj):
#         return obj.seller.email
#

# admin.site.register(ProcessQueue, EmailAdmin)

# Register your models here.
admin.site.register(Auction, AuctionAdmin)
admin.site.register(BidAuction, BidAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
