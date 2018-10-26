from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from datetime import datetime
from django.test import Client
from newApp.models import *
# from .views import email_view

# Create your tests here.

# Create your tests here.
class CreateAuctionTest(TestCase):
    # fixtures = ['db_data.json',]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='abc', email='abc@abo.fi', password='abc')

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homePage/show.html")
    #
    # def test_redirectMe(self):
    #     resp = self.client.get(reverse("to_home"))
    #     self.assertRedirects(resp,reverse("home"))

    def test_post(self):
        print("Testing posting")
        pre_count = Auction.objects.count()
        print("Before creating an auction in a test:", pre_count)

        # Try to add a new auction without authenticating user
        response = self.client.post(reverse("add_auction"), {'auctioTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("login") in response.url)

        # Try to add a new auction after authenticating user
        self.client.login(username="abc", password="abc")
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        self.assertEqual(response.status_code, 200)

        # Post back Yes to the confirmation form
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})

        post_count = Auction.objects.count()
        print("After creating an auction in a test:", post_count)

        self.assertEqual(pre_count+1, post_count)
        self.assertRedirects(response, reverse("home"))

    def test_decline_confirmation(self):
        print("Testing confirmation")

        pre_count = Auction.objects.count()
        print("Before creating an auction in a test:", pre_count)

        # Try to add a new auction after authenticating user
        self.client.login(username="abc", password="abc")
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        self.assertEqual(response.status_code, 200)

        # Post back No to the confirmation form
        response = self.client.post(reverse("save_auction"), {'option': 'No', })

        post_count = Auction.objects.count()
        print("After creating an auction in a confirmation test:", post_count)

        self.assertEqual(pre_count, post_count)
        self.assertRedirects(response, reverse("home"))

    def test_email(self):
        self.client.login(username="abc", password="abc")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        count = Email.objects.count()
        print("After creating an auction email count " + str(count))
        self.assertEqual(count,1)

class BidTest(TestCase):
    # fixtures = ['db_data.json',]
    def setUp(self):
        self.client = Client()
        # self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='abc', email='abc@abo.fi', password='abc')
        self.bidder = get_user_model().objects.create_user(
            username='bidder', email='bidder@abo.fi', password='bidder')

    # def test_load_bidpage(self):
    #     response = self.client.get('AuctionHandler/bidAuction.html')
    #     self.failUnlessEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "homePage/show.html")
    #
    # def test_redirectMe(self):
    #     resp = self.client.get(reverse("to_home"))
    #     self.assertRedirects(resp,reverse("home"))
    def test_load_bidpage(self):
        response = self.client.get('AuctionHandler/bidAuction.html')
        self.assertEqual(response.status_code, 404)
        # self.assertTrue(reverse("home") in response.url)

    def test_bid(self):
        print("Testing bidding")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="bidder", password="bidder")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        self.client.logout()
        auctionId = Auction.objects.all().last().id
        # Try to add a new bid without authenticating user
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("login") in response.url)

        # Try to add a new bid with new user and value higher than minimum price after authenticating user
        self.client.login(username="abc", password="abc")
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("home") in response.url)

        post_count = BidAuction.objects.count()
        print("After bidding in a test:", post_count)

        self.assertEqual(pre_count+1, post_count)
        self.assertRedirects(response, reverse("home"))

    def test_bidding_as_seller(self):
        print("Testing bidding as seller ")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="bidder", password="bidder")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        auctionId = Auction.objects.all().last().id

        # Try to access a new bid as a seller
        response = self.client.get(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("home"))

        # Try to add a new bid as seller
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        post_count = BidAuction.objects.count()
        print("After bidding in as a seller:", post_count)

        self.assertEqual(pre_count, post_count)

    def test_bidding_as_highestBidder(self):
        print("--------Testing bidding as highest bidder--------")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="abc", password="abc")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        auctionId = Auction.objects.all().last().id
        self.client.logout()
        # Add a new bid
        self.client.login(username="bidder", password="bidder")
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        # Add a new bid as highest bidder
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        post_count = BidAuction.objects.count()
        print("After bidding in as a highest bidder:", post_count)

        self.assertEqual(pre_count, post_count)

        def test_email(self):
            self.client.login(username="abc", password="abc")
            #Add auction
            response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
            #Confirm auction
            response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
            self.client.logout()
            self.client.login(username="bidder", password="bidder")
            auctionId = Auction.objects.all().last().id
            # Try to add a new bid without authenticating user
            response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})

            count = Email.objects.count()
            print("After creating an auction email count " + str(count))
            self.assertEqual(count,2)

class ConcurrentSessionsTest(TestCase):
    # fixtures = ['db_data.json',]
    def setUp(self):
        self.client = Client()
        # self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='abc', email='abc@abo.fi', password='abc')
        self.bidder = get_user_model().objects.create_user(
            username='bidder', email='bidder@abo.fi', password='bidder')

    # def test_load_bidpage(self):
    #     response = self.client.get('AuctionHandler/bidAuction.html')
    #     self.failUnlessEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "homePage/show.html")
    #
    # def test_redirectMe(self):
    #     resp = self.client.get(reverse("to_home"))
    #     self.assertRedirects(resp,reverse("home"))
    def test_load_bidpage(self):
        response = self.client.get('AuctionHandler/bidAuction.html')
        self.assertEqual(response.status_code, 404)
        # self.assertTrue(reverse("home") in response.url)

    def test_bid(self):
        print("Testing bidding")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="bidder", password="bidder")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        self.client.logout()
        auctionId = Auction.objects.all().last().id
        # Try to add a new bid without authenticating user
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("login") in response.url)

        # Try to add a new bid with new user and value higher than minimum price after authenticating user
        self.client.login(username="abc", password="abc")
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("home") in response.url)

        post_count = BidAuction.objects.count()
        print("After bidding in a test:", post_count)

        self.assertEqual(pre_count+1, post_count)
        self.assertRedirects(response, reverse("home"))

    def test_bidding_as_seller(self):
        print("Testing bidding as seller ")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="bidder", password="bidder")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        auctionId = Auction.objects.all().last().id

        # Try to access a new bid as a seller
        response = self.client.get(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("home"))

        # Try to add a new bid as seller
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        post_count = BidAuction.objects.count()
        print("After bidding in as a seller:", post_count)

        self.assertEqual(pre_count, post_count)

    def test_bidding_as_highestBidder(self):
        print("--------Testing bidding as highest bidder--------")
        pre_count = BidAuction.objects.count()
        print("Before bidding an auction in a test:", pre_count)

        self.client.login(username="abc", password="abc")
        #Add auction
        response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
        #Confirm auction
        response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
        auctionId = Auction.objects.all().last().id
        self.client.logout()
        # Add a new bid
        self.client.login(username="bidder", password="bidder")
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        # Add a new bid as highest bidder
        response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}))
        self.assertEqual(response.status_code, 200)

        post_count = BidAuction.objects.count()
        print("After bidding in as a highest bidder:", post_count)

        self.assertEqual(pre_count, post_count)

        def test_email(self):
            self.client.login(username="abc", password="abc")
            #Add auction
            response = self.client.post(reverse("add_auction"), {'auctionTitle': 'my title', 'description': 'my body', 'minimumPrice': '10.00',})
            #Confirm auction
            response = self.client.post(reverse("save_auction"), {'option': 'Yes', 'title': 'my title', 'description': 'my body', 'minPrice': '10.00',})
            self.client.logout()
            self.client.login(username="bidder", password="bidder")
            auctionId = Auction.objects.all().last().id
            # Try to add a new bid without authenticating user
            response = self.client.post(reverse("bid_auction", kwargs={'id':auctionId}), {'value': '11.00',})

            count = Email.objects.count()
            print("After creating an auction email count " + str(count))
            self.assertEqual(count,2)
