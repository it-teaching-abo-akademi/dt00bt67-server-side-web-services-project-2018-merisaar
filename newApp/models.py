from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

class BlogModel(models.Model):
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    body = models.TextField()
    def __str__(self):
        return self.title

<<<<<<< HEAD
class Auction(models.Model):
    seller = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    auctionTitle = models.CharField(max_length=150)
    description = models.TextField()
    minimumPrice = models.DecimalField(max_digits=5, decimal_places=2)
    deadline = models.DateTimeField(blank=True)
    def __str__(self):
        return self.title

# class User(AbstractUser):
#     pass
# class User(models.Model):
#     username = models.CharField(max_length=150)
#     email = models.EmailField()
#     password = models.CharField(max_length=150)
#     timestamp = models.DateTimeField()
#     def __str__(self):
#         return self.title
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=25, unique=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     objects = UserManager()
#     REQUIRED_FIELDS ["email"]
#     def __str__(self):
#         return "@{}".format(self.username)
#
#     def get_short_name(self):
#         return self.alias
#     def get_long_name(self):
#         return "{} @{}".format(self.alias, self.username)
=======
class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.title
>>>>>>> 9de138323cfce2e4640dc640cbdd4acc0774de2f