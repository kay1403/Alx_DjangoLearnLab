from django.urls import path
from .views import list_books
from .views import LibraryDetailView

from .views import (
    add_book, edit_book, delete_book,
    admin_view, librarian_view, member_view,
    register_view, login_view, logout_view
)

urlpatterns = [
    # --- BOOK VIEWS ---
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', delete_book, name='delete_book'),

    # --- ROLE-BASED VIEWS ---
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # --- AUTH VIEWS (EXIGÉ PAR ALX) ---
    path('register/', views.register, name='register'),
    path(
        'login/',
        LoginView.as_view(template_name='relationship_app/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='relationship_app/logout.html'),
        name='logout'
    ),
]