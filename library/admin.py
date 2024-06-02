from django.contrib import admin
from django.contrib.auth import get_user_model

from library.models import Book, Library, UserProfile


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
