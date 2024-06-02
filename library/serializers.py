from django.contrib.auth.models import User
from rest_framework import serializers

from library.models import Library, Book, UserProfile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'year', 'category', 'isbn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', )


class LibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Library
        fields = ('name', 'city', 'address')
