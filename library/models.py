from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['address']),
        ]

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')


class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    category = models.CharField(max_length=16)
    isbn = models.CharField(max_length=13, unique=True)

    libraries = models.ManyToManyField(Library,
                                       related_name='books',
                                       blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['title']),
            models.Index(fields=['year']),
            models.Index(fields=['category']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return self.title
