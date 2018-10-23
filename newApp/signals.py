from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.utils import translation

@receiver(user_logged_in)
def update_language(sender, user, request, **kwargs):
    translation.activate(request.user.language)
    request.session[translation.LANGUAGE_SESSION_KEY] = request.user.language

@receiver(user_logged_out)
def update_language(sender, request, **kwargs):
    translation.activate('en')
    request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
