from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from datetime import datetime
from blogApp.models import Blog
from .views import email_view

# Create your tests here.

# Create your tests here.
class SimpleTest(TestCase):
    fixtures = ['db_data.json',]

    def setUp(self):
        self.user = User.objects.create_user(
            username='abc', email='abc@abo.fi', password='abc')

    def test_archive(self):
        response = self.client.get(reverse('home'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "archive.html")

    def test_redirectMe(self):
        resp = self.client.get(reverse("to_home"))
        self.assertRedirects(resp,reverse("home"))

    def test_post(self):
        pre_count = Blog.objects.count()
        print("Before creating a blog in a test:", pre_count)

        # Try to add a new blog without authenticating user
        response = self.client.post(reverse("add_blog"), {'title': 'my title', 'body': 'my body',})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("login") in response.url)

        # Try to add a new blog after authenticating user
        self.client.login(username="abc", password="abc")
        response = self.client.post(reverse("add_blog"), {'title': 'my title', 'body': 'my body',})
        self.assertEqual(response.status_code, 200)

        # Post back Yes to the confirmation form
        response = self.client.post(reverse("save_blog"), {'option': 'Yes', 'b_title': 'my title', 'b_body': 'my body',})

        post_count = Blog.objects.count()
        print("After creating a blog in a test:", post_count)

        self.assertEqual(pre_count+1, post_count)
        self.assertRedirects(response, reverse("home"))

    def test_email(self):
        self.client.login(username="abc", password="abc")
        response = self.client.get(reverse("email"))
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject, 'Test Email Subject')


class SimpleTestWithFactory(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='abc', email='abc@abo.fi', password='abc')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/authview/')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        response = email_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email sent")

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = email_view(request)

        self.assertEqual(response.status_code, 302)
