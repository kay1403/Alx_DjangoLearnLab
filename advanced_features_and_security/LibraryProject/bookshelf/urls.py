from django.urls import path
from .views import book_list, create_book, edit_book, delete_book,form_example_view

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('book/create/', create_book, name='create_book'),
    path('book/edit/<int:pk>/', edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', delete_book, name='delete_book'),
    path('form-example/', form_example_view, name='form_example'),

]
