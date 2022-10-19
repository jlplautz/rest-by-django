from http import HTTPStatus

import pytest

from django.shortcuts import resolve_url
from pyprg.core.models import Author, Book

CT_JSON = 'application/json'

pytestmark = pytest.mark.django_db
list_authors_url = resolve_url('core:list-authors')


@pytest.fixture
def book(db):
    author = Author.objects.create(name='Luciano Ramalho')
    book = Book.objects.create(
        name='Python Fluente',
        edition=2,
        publication_year=2022
    )
    book.authors.add(author)
    return book


def test_list_all_author(client):
    Author.objects.bulk_create(Author(name=f'Author {i}') for i in range(10))

    response = client.get(list_authors_url, data={'page': 2, 'page_size': 5})

    # teste muito fraco -> verifica somente o status code
    assert response.status_code == HTTPStatus.OK
    # teste para verificar o numero de paginas
    assert response.json()['num_pages'] == 2
    assert 5 == len(response.json()['data'])

    # assert response.json()['data'][0] == [{'id': 1, 'name': 'Author 0'}]
    # teste de comparação dos 5 ulimos registros
    assert [a['name'] for a in response.json()['data']] == [f'Author {i}' for i in range(5, 10)]


def test_search_author_by_name(client):
    author1 = Author.objects.create(name='J.K Rowling')
    Author.objects.create(name='David Beazley')

    response = client.get(list_authors_url, data={'q': 'rowling'})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['data'] == [{'id': author1.id, 'name': 'J.K Rowling'}]


def test_search_author_by_name_without_match(client):
    Author.objects.create(name='David Beazley')

    response = client.get(list_authors_url, data={'q': 'no match'})

    assert response.status_code == HTTPStatus.OK
    # como resposta do no match vamos ter uma lista vazia
    assert response.json()['data'] == []


def test_create_book(client):
    author = Author.objects.create(name='Luciano Ramalho')
    data = {
        "name": 'Python Fluente',
        "edition": 2,
        "publication_year": 2022,
        "authors": [author.id]
    }

    # response esta inserindo um content_type= Application/json e portanto
    # na view a informação vai chegar no request.body, para isto é necessario
    # fazer a tratativa com import json
    response = client.post('/api/books/', data=data, content_type=CT_JSON)

    assert response.status_code == HTTPStatus.CREATED

    # first retorna None se não existir book na table
    book = Book.objects.first()
    assert book is not None

    assert response['Location'] == f'/api/books/{book.id}/'

    response_data = response.json()
    assert response_data['name'] == 'Python Fluente'
    assert response_data['edition'] == 2
    assert response_data['publication_year'] == 2022
    assert response_data['authors'] == [author.id]
    assert response_data['id'] == book.id


def test_read_book(client, book):
    # author = Author.objects.create(name='Luciano Ramalho')
    # book = Book.objects.create(
    #     name='Python Fluente',
    #     edition=2,
    #     publication_year=2022
    # )
    # book.authors.set([author])

    response = client.get(f'/api/books/{book.id}/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == book.to_dict()


def test_read_unexist_book(client):
    response = client.get('/api/books/10/')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_book(client, book):
    data = {
        "id": book.id,
        "name": 'Python Fluente',
        "edition": 3,
        "publication_year": 2024,
        "authors": [a.id for a in book.authors.all()]
    }

    response = client.put(f'/api/books/{book.id}/', data=data, content_type=CT_JSON)

    assert response.status_code == HTTPStatus.OK

    assert response.json() == data


def test_update_book_author2(client, book):
    author_2 = Author.objects.create(name='Reznzo')
    data = {
        "id": book.id,
        "name": 'Python Fluente',
        "edition": 3,
        "publication_year": 2024,
        "authors": [author_2.pk]
    }

    response = client.put(f'/api/books/{book.id}/', data=data, content_type=CT_JSON)

    assert response.status_code == HTTPStatus.OK

    assert response.json() == data


def test_update_unexist_book(client):
    response = client.get('/api/books/10/', data={}, content_type=CT_JSON)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_book(client, book):
    response = client.delete(f'/api/books/{book.id}/')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert not Book.objects.filter(pk=book.id).exists()


def test_delete_unexist_book(client):
    response = client.delete('/api/books/10/', data={}, content_type=CT_JSON)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_books(client, book):
    response = client.get('/api/books/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [book.to_dict()]
