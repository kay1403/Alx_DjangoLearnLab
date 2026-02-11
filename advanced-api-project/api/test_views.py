from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.author = Author.objects.create(name="Frank Herbert")
        self.book = Book.objects.create(
            title="Dune", 
            publication_year=1965, 
            author=self.author
        )

    def test_list_books(self):
        """Verify that any user can list books."""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_unauthenticated(self):
        """Verify that unauthenticated users cannot create books."""
        data = {"title": "New Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Verify that authenticated users can create books."""
        self.client.login(username='testuser', password='password123')
        data = {"title": "Children of Dune", "publication_year": 1976, "author": self.author.id}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)