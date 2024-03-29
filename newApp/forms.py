from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Auction, BidAuction
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CreateAuctionForm(forms.ModelForm):
        class Meta:
            model = Auction
            fields = ['auctionTitle', 'description', 'minimumPrice']


class ConfAuctionForm(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES)
    title = forms.CharField(widget=forms.HiddenInput())
    description = forms.CharField(widget=forms.HiddenInput())
    minPrice = forms.DecimalField(widget=forms.HiddenInput())

class EditAuctionForm(forms.ModelForm):
        class Meta:
            model = Auction
            fields = ['description']

class BidAuctionForm(forms.ModelForm):
        class Meta:
            model = BidAuction
            fields = ['value']


class CopyOfForm(forms.Form):
    CHOICES = [(x,x) for x in ("yes", "no")]
    option = forms.ChoiceField(choices=CHOICES)
    c_title = forms.CharField(widget=forms.HiddenInput())
    c_body = forms.CharField(widget=forms.HiddenInput())

class UserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = get_user_model().objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = get_user_model().objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):

        password = self.cleaned_data.get('password')

        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],

            self.cleaned_data['password']

        )
        return user
