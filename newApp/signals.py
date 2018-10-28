from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import post_save
from .models import BidAuction
from django.utils import translation

@receiver(user_logged_in)
def update_language(sender, user, request, **kwargs):
    translation.activate(request.user.language)
    request.session[translation.LANGUAGE_SESSION_KEY] = request.user.language

@receiver(user_logged_out)
def update_language_logged_out(sender, request, **kwargs):
    translation.activate('en')
    request.session[translation.LANGUAGE_SESSION_KEY] = 'en'

@receiver(post_save, sender=BidAuction)
def update_auction_totals_for_bid(sender, instance, created, **kwargs):
    if created:
        auction = instance.auction
        auction.minimumPrice = instance.value
        auction.save()
