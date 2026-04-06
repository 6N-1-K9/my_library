from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookModelTest(TestCase):
    def test_book_str_returns_expected_string(self):
        book = Book.objects.create(
            title="1984",
            author="Джордж Оруэлл",
            year=1949,
        )

        expected = "1984 — Джордж Оруэлл (1949)"
        self.assertEqual(str(book), expected)


class BookViewsTest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="1984",
            author="Джордж Оруэлл",
            year=1949,
        )
        self.book2 = Book.objects.create(
            title="Скотный двор",
            author="Джордж Оруэлл",
            year=1945,
        )
        self.book3 = Book.objects.create(
            title="Война и мир",
            author="Лев Толстой",
            year=1869,
        )

    def test_book_list_page_returns_200(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)

    def test_book_list_page_shows_all_books(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")
        self.assertContains(response, "Скотный двор")
        self.assertContains(response, "Война и мир")

    def test_book_create_get_returns_200(self):
        response = self.client.get(reverse("book_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добавить книгу")

    def test_book_create_post_creates_book_and_redirects(self):
        books_count_before = Book.objects.count()

        response = self.client.post(
            reverse("book_create"),
            data={
                "title": "Мастер и Маргарита",
                "author": "Михаил Булгаков",
                "year": 1967,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("book_list"))
        self.assertEqual(Book.objects.count(), books_count_before + 1)

        created_book = Book.objects.get(title="Мастер и Маргарита")
        self.assertEqual(created_book.author, "Михаил Булгаков")
        self.assertEqual(created_book.year, 1967)

    def test_book_edit_get_returns_200(self):
        response = self.client.get(reverse("book_edit", args=[self.book1.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Редактировать книгу")

    def test_book_edit_post_updates_book_and_redirects(self):
        response = self.client.post(
            reverse("book_edit", args=[self.book1.pk]),
            data={
                "title": "1984",
                "author": "Оруэлл",
                "year": 1950,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("book_list"))

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "1984")
        self.assertEqual(self.book1.author, "Оруэлл")
        self.assertEqual(self.book1.year, 1950)

    def test_book_delete_post_deletes_book_and_redirects(self):
        books_count_before = Book.objects.count()

        response = self.client.post(reverse("book_delete", args=[self.book1.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("book_list"))
        self.assertEqual(Book.objects.count(), books_count_before - 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_book_search_by_title_returns_matching_books(self):
        response = self.client.get(
            reverse("book_list"),
            data={"title": "1984"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")
        self.assertNotContains(response, "Скотный двор")
        self.assertNotContains(response, "Война и мир")

    def test_book_search_by_author_returns_matching_books(self):
        response = self.client.get(
            reverse("book_list"),
            data={"author": "Оруэлл"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")
        self.assertContains(response, "Скотный двор")
        self.assertNotContains(response, "Война и мир")

    def test_book_search_by_year_returns_matching_books(self):
        response = self.client.get(
            reverse("book_list"),
            data={"year": 1869},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Война и мир")
        self.assertNotContains(response, "1984")
        self.assertNotContains(response, "Скотный двор")

    def test_book_search_with_empty_filters_returns_all_books(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")
        self.assertContains(response, "Скотный двор")
        self.assertContains(response, "Война и мир")