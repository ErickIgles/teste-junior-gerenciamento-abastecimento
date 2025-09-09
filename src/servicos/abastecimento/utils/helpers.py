from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from django.core.paginator import Paginator

from ..models import RegistroReabastecimento


def reverter_reabastecimento(obj):
    """
     Reverte um reabastecimento removendo a quantidade do tanque.
    """

    tanque = obj.tanque

    tanque.quantidade_disponivel -= obj.quantidade

    if tanque.quantidade_disponivel < 0:

        tanque.quantidade = 0

    tanque.save()


def ajustar_next_url(next_url):

    registros = RegistroReabastecimento.objects.all().order_by('-criado')

    paginator = Paginator(registros, 6)

    parsed = urlparse(next_url)

    query = parse_qs(parsed.query)

    page = int(query.get('page', ['1'])[0])

    try:
        page = page

    except (ValueError, TypeError):

        page = 1

    if page >= paginator.num_pages:

        page = paginator.num_pages if paginator.num_pages > 0 else 1

    elif page < 1:
        page = 1

    query['page'] = [str(page)]

    new_query = urlencode(query, doseq=True)

    new_parsed = parsed._replace(query=new_query)

    return urlunparse(new_parsed)
