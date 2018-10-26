from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from datetime import datetime
from newApp.models import *
# from .views import email_view

# Create your tests here.

# Create your tests here.
class UC3Test(TestCase):
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
        print("After creating an auction in a test:", post_count)

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

#
# class SimpleTestWithFactory(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='abc', email='abc@abo.fi', password='abc')
#
#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/authview/')
#
#         # Recall that middleware are not supported. You can simulate a
#         # logged-in user by setting request.user manually.
#         request.user = self.user
#         response = email_view(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Email sent")
#
#         # Or you can simulate an anonymous user by setting request.user to
#         # an AnonymousUser instance.
#         request.user = AnonymousUser()
#
#         # Test my_view() as if it were deployed at /customer/details
#         # response = email_view(request)
#
#         self.assertEqual(response.status_code, 302)
