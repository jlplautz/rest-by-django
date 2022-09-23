from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def to_dict(self):
        # para transforma o object Author em um dicionario
        return {
            'id': self.id,
            'name': self.name
        }


class Book(models.Model):
    name = models.CharField(max_length=128)
    edition = models.PositiveIntegerField()
    publication_year = models.CharField(max_length=4)
    # um autor pode ter varios livros/um livro pode ter varios autores
    # um livro não pode existir se não ter um autor portanto blank=False
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.name
