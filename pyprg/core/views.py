import json
from http import HTTPStatus

# from unicodedata import name
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, resolve_url
from pyprg.core.models import Author, Book

DEFAULT_PAGE_SIZE = 25


def authors(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)
    q = request.GET.get('q')

    queryset = Author.objects.all()
    if q:
        # lockup do Django _icontains
        queryset = queryset.filter(name__icontains=q)

    paginator = Paginator(queryset, per_page=page_size)
    page = paginator.get_page(page_number)

    return JsonResponse({
        'data': [a.to_dict() for a in page.object_list],
        'count': paginator.count,
        # se não transformar pata int vai aparecer como char
        'current_page': int(page_number),
        'num_pages': paginator.num_pages
    })


def book_list_create(request):

    if request.method == 'POST':
        # loads -> faz a serialização de str, bytes e bytearray
        # load  -> faz a serialização de qualquer coisa que use .read()
        # utilizamos o load pois o request tem o file-like (suporta o .read())
        payload = json.load(request)

        authors = payload.pop('authors')
        # passar o payload como argumentos nomeados
        book = Book.objects.create(**payload)
        book.authors.set(authors)

        # JsonResponse tem que reportar um dicionario que foi serializado no models
        response = JsonResponse(book.to_dict(), status=HTTPStatus.CREATED)
        # informamos a localização do recurso criado
        response['Location'] = resolve_url(book)
    else:
        books = Book.objects.all()
        data = [b.to_dict() for b in books]
        # JsonResponse por padrão só aceita dicionario e estavamos passando uma lista
        # return JsonResponse(data) e portanto pelo que colocar safe=False
        return JsonResponse(data, safe=False)

    return response


def book_read_update_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    handlers = {
        'GET': _book_read,
        'PUT': _book_update,
        'DELETE': _book_delete
    }
    try:
        handler = handlers[request.method]
    except KeyError:
        return HttpResponseNotAllowed()
    else:
        return handler(request, book)


def _book_read(request, book):
    # função book_read recebe um livro e retorna um Jsonreponse
    return JsonResponse(book.to_dict())


def _book_update(request, book):
    # função book_update recebe um livro e retorna um Jsonreponse
    payload = json.load(request)
    book.name = payload['name']
    book.edition = payload['edition']
    book.publication_year = payload['publication_year']
    book.save()
    book.authors.set(payload['authors'])
    return JsonResponse(book.to_dict())


def _book_delete(request, book):
    # função book_delete recebe um livro e retorna um Jsonreponse
    book.delete()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)
