import json
from http import HTTPStatus
from django.db.models import Q

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

    return JsonResponse(page2dict(page))


def page2dict(page):
    # vai recebe a pagina e transformar em um dict
    return {
        'data': [obj.to_dict() for obj in page],
        'count': page.paginator.count,
        # se não transformar para int vai aparecer como char
        'current_page': page.number,
        'num_pages': page.paginator.num_pages
    }


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
        return response
    else:
        # pegar a pagina e tamanho da pagiba que foi solicitado
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

        filters = Q()

        # filtro com parametro 'publication_year'
        # caso o publication_year seja passado na url podemos fazer o filtro
        # abaixo um operator novo no python walrus -> podemos atribuir o valor a uma varialvel
        # e retornar este valor na mesma expressão
        if publication_year := request.GET.get('publication_year'):
            filters |= Q(publication_year=publication_year)

        # filtro para author
        if author_id := request.GET.get('author'):
            filters |= Q(authors=author_id)

        queryset = Book.objects.filter(filters).order_by('name')

        # fazemos a paginação do queryset, aplicando o limite do offset
        paginator = Paginator(queryset, per_page=page_size)
        page = paginator.get_page(page_number)
        # serialização da resposta
        return JsonResponse(page2dict(page))

        # JsonResponse por padrão só aceita dicionario e estavamos passando uma lista
        # return JsonResponse(data) e portanto pelo que colocar safe=False


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
