from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pyprg.core.models import Author

pytestmark = pytest.mark.django_db
list_authors_url = resolve_url('core:list-authors')


def test_list_all_authors(client):
    Author.objects.bulk_create(Author(name=f'Author {i}') for i in range(10))

    response = client.get(list_authors_url, data={'page': 2, 'page_size': 5})

    # teste muito fraco -> verifica somente o status code
    assert response.status_code == HTTPStatus.OK
    assert response.json()['num_pages'] == 2
    assert 5 == len(response.json()['data'])

    # assert response.json()['data'][0] == [{'id': 1, 'name': 'Author 0'}]
    assert [a['name'] for a in response.json()['data']] == [f'Author {i}' for i in range(5, 10)]
