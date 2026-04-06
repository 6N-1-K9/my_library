from django.db import models


class Book(models.Model):
    title = models.CharField("Название", max_length=255)
    author = models.CharField("Автор", max_length=255)
    year = models.PositiveIntegerField("Год выпуска")

    def __str__(self):
        return f"{self.title} — {self.author} ({self.year})"