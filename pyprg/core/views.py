
from django.core.paginator import Paginator
from django.http import JsonResponse
from pyprg.core.models import Author

DEFAULT_PAGE_SIZE = 25


def authors(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', DEFAULT_PAGE_SIZE)

    paginator = Paginator(Author.objects.all(), per_page=page_size)
    page = paginator.get_page(page_number)

    return JsonResponse({
        'data': [a.to_dict() for a in page.object_list],
        'count': paginator.count,
        'current_page': page_number,
        'num_pages': paginator.num_pages
    })
