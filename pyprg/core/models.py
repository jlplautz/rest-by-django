from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=128)
    edition = models.PositiveIntegerField()
    publication_year = models.CharField(max_length=4)
    # um livro pode ter varios autores/autores podem ter varios livros
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.name
