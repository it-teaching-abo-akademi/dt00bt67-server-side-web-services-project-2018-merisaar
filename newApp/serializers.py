from rest_framework import serializers
from newApp.models import *
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class AuctionShortSerializer(serializers.ModelSerializer):
    # seller = fields.ForeignKey(User, 'rental', full=False, null=True, blank=True)
    class Meta:
        model = Auction
        fields = ('id', 'active', 'auctionTitle', 'seller')

class AuctionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'active', 'seller', 'auctionTitle', 'description', 'minimumPrice', 'deadline', 'banned')

class BidAuctionSerializer(serializers.ModelSerializer):
    auction = AuctionDetailSerializer()
    bidder = UserSerializer()

    class Meta:
        model = BidAuction
        fields = ('id', 'value', 'auction', 'bidder', )

    def create(self, validated_data):
        bidder_data = validated_data.pop('bidder')
        value = validated_data.pop('value')
        auction_data = validated_data.pop('auction')
        username = bidder_data.pop('username')
        auctionTitle= auction_data.pop('auctionTitle')
        deadline= auction_data.pop('deadline')
        seller= auction_data.pop('seller')
        bidder = get_user_model().objects.filter(username=username).first()
        if not bidder:
            raise serializers.ValidationError('User does not exist.')
        auction = Auction.objects.filter(auctionTitle=auctionTitle, deadline=deadline, seller=seller).first()
        if not auction:
            raise serializers.ValidationError('Auction does not exist. Required fields: auctionTitle, deadline and seller.')
        if value< auction.minimumPrice:
            raise serializers.ValidationError('Bid is too low. Must be over minimum bid of ' + str(auction.minimumPrice))
        bid = BidAuction.objects.create(bidder = bidder, auction=auction, **validated_data)
        return bid

    # def save(self):
    #     bidder = CurrentUserDefault()
    #     value = self.validated_data['title']
    #     auction = self.validated_data['auction']
