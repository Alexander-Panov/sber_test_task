from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from library.models import Book, Library, UserProfile
from library.serializers import BookSerializer, LibrarySerializer, UserProfileSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # select_related
        'library_users_list': reverse('library:library_users_list', kwargs={'library_id': 1},
                                      request=request, format=format),
        'user_books_list': reverse('library:user_books_list', kwargs={'user_id': 1},
                                   request=request, format=format),
        # prefetch_related
        'city_library_books': reverse('library:city_library_books', request=request, format=format) + "?city=SPB",
        'book_libraries': reverse('library:book_libraries', kwargs={'isbn': 1234567890124},
                                  request=request, format=format),
        # Prefetch
        'library_authors_books': reverse('library:library_authors_books', kwargs={'library_id': 1},
                                         request=request, format=format) + "?author=Mark%20Twain",
        'book_city_users': reverse('library:book_city_users', kwargs={'isbn': 1234567890124},
                                   request=request, format=format) + "?city=SPB",
    })


""" select_related """


class LibraryUsersListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        library_id = self.kwargs['library_id']
        user_profiles = UserProfile.objects.select_related('library').filter(library__id=library_id)
        return user_profiles


class UserBooksListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        try:
            user = (UserProfile.objects.select_related('library')
                    .prefetch_related('library__books')
                    .get(id=user_id))
        except UserProfile.DoesNotExist:
            return []

        return user.library.books.all()


""" prefetch_related """


class CityLibraryBooksListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        city = self.request.query_params.get('city')
        libraries = Library.objects
        if city is not None:
            libraries = libraries.filter(city=city)

        libraries = libraries.prefetch_related('books')

        book_ids = set()
        for library in libraries:
            for book in library.books.all():
                book_ids.add(book.id)
        return Book.objects.filter(id__in=book_ids).distinct()


class BookLibrariesListView(generics.ListAPIView):
    serializer_class = LibrarySerializer

    def get_queryset(self):
        isbn = self.kwargs['isbn']
        try:
            book = Book.objects.prefetch_related('libraries').get(isbn=isbn)
        except Book.DoesNotExist:
            return []

        return book.libraries.all()


""" Prefetch """


class AuthorBooksListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        library_id = self.kwargs['library_id']
        author = self.request.query_params.get('author')

        queryset = Book.objects.filter(author=author) if author is not None else Book.objects.all()

        try:
            author_books = (Library.objects.prefetch_related(Prefetch('books', queryset=queryset))
                            .get(id=library_id).books.all())
        except Library.DoesNotExist:
            return []
        return author_books


class BookCityUsersListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        isbn = self.kwargs['isbn']
        city = self.request.query_params.get('city')

        queryset = Library.objects.filter(city=city) if city is not None else Library.objects.all()

        try:
            book = (Book.objects.prefetch_related(Prefetch('libraries__users__user', queryset=queryset))
                    .get(isbn=isbn))
        except Book.DoesNotExist:
            return []

        user_ids = set()
        for library in book.libraries.all():
            for user in library.users.all():
                user_ids.add(user.id)
        return UserProfile.objects.filter(id__in=user_ids)
