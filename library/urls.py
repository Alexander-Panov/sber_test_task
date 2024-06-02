from django.urls import path

from library import views

app_name = "library"

urlpatterns = [
    path('', views.api_root),
    # select_related
    path('library/<int:library_id>/users', views.LibraryUsersListView.as_view(), name='library_users_list'),
    path('user/<int:user_id>/books', views.UserBooksListView.as_view(), name='user_books_list'),
    # prefetch_related
    path('books/', views.CityLibraryBooksListView.as_view(), name='city_library_books'),
    path('books/<int:isbn>/libraries', views.BookLibrariesListView.as_view(), name='book_libraries'),
    # Prefetch
    path('library/<int:library_id>/books', views.AuthorBooksListView.as_view(), name='library_authors_books'),
    path('books/<int:isbn>/users', views.BookCityUsersListView.as_view(), name='book_city_users'),
]
