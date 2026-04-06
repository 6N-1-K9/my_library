from django.core.management.base import BaseCommand
from library.models import Book


BOOKS = [
    {"title": "Война и мир", "author": "Лев Толстой", "year": 1869},
    {"title": "Анна Каренина", "author": "Лев Толстой", "year": 1877},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "year": 1866},
    {"title": "Идиот", "author": "Фёдор Достоевский", "year": 1869},
    {"title": "Братья Карамазовы", "author": "Фёдор Достоевский", "year": 1880},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967},
    {"title": "Собачье сердце", "author": "Михаил Булгаков", "year": 1925},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "year": 1833},
    {"title": "Капитанская дочка", "author": "Александр Пушкин", "year": 1836},
    {"title": "Герой нашего времени", "author": "Михаил Лермонтов", "year": 1840},
    {"title": "Мёртвые души", "author": "Николай Гоголь", "year": 1842},
    {"title": "Ревизор", "author": "Николай Гоголь", "year": 1836},
    {"title": "Отцы и дети", "author": "Иван Тургенев", "year": 1862},
    {"title": "Дворянское гнездо", "author": "Иван Тургенев", "year": 1859},
    {"title": "Обломов", "author": "Иван Гончаров", "year": 1859},
    {"title": "Чайка", "author": "Антон Чехов", "year": 1896},
    {"title": "Вишнёвый сад", "author": "Антон Чехов", "year": 1904},
    {"title": "Палата №6", "author": "Антон Чехов", "year": 1892},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "year": 1940},
    {"title": "Доктор Живаго", "author": "Борис Пастернак", "year": 1957},
    {"title": "Мы", "author": "Евгений Замятин", "year": 1924},
    {"title": "12 стульев", "author": "Илья Ильф и Евгений Петров", "year": 1928},
    {"title": "Золотой телёнок", "author": "Илья Ильф и Евгений Петров", "year": 1931},
    {"title": "1984", "author": "Джордж Оруэлл", "year": 1949},
    {"title": "Скотный двор", "author": "Джордж Оруэлл", "year": 1945},
    {"title": "Убить пересмешника", "author": "Харпер Ли", "year": 1960},
    {"title": "Над пропастью во ржи", "author": "Джером Сэлинджер", "year": 1951},
    {"title": "451 градус по Фаренгейту", "author": "Рэй Брэдбери", "year": 1953},
    {"title": "Марсианские хроники", "author": "Рэй Брэдбери", "year": 1950},
    {"title": "Цветы для Элджернона", "author": "Дэниел Киз", "year": 1966},
]


class Command(BaseCommand):
    help = "Заполняет базу данных книгами"

    def handle(self, *args, **options):
        created_count = 0

        for book_data in BOOKS:
            _, created = Book.objects.get_or_create(
                title=book_data["title"],
                author=book_data["author"],
                year=book_data["year"],
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Добавлено новых книг: {created_count}. Всего книг в базе: {Book.objects.count()}."
            )
        )
