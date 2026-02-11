from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

        self.author = Author.objects.create(name="Frank Herbert")

        self.book = Book.objects.create(
            title="Dune",
            publication_year=1965,
            author=self.author
        )

    def test_list_books(self):
        """Test retrieving list of books"""
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Dune")

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated user cannot create book"""
        url = reverse('book-list')

        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Test authenticated user can create book"""
        self.client.login(username='testuser', password='password123')

        url = reverse('book-list')

        data = {
            "title": "Children of Dune",
            "publication_year": 1976,
            "author": self.author.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Children of Dune")
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test updating a book"""
        self.client.login(username='testuser', password='password123')

        url = reverse('book-detail', args=[self.book.id])

        data = {
            "title": "Dune Messiah",
            "publication_year": 1969,
            "author": self.author.id
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Dune Messiah")

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='password123')

        url = reverse('book-detail', args=[self.book.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
