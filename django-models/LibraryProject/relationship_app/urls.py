from django.urls import path
from .views import (
    list_books, LibraryDetailView, add_book, edit_book, delete_book,
    admin_view, librarian_view, member_view
)

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('book/add/', add_book, name='add_book'),
    path('book/edit/<int:pk>/', edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', delete_book, name='delete_book'),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]
