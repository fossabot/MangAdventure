from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from reader.models import Chapter, Series


def json_error(message, status=500):
    return JsonResponse({'error': message, 'status': status}, status=status)


def _chapter_response(request, _chapter, json=True):
    response = {
        'title': _chapter.title,
        'url': request.build_absolute_uri(
            reverse('reader:chapter',
                    args=[_chapter.series.slug,
                          _chapter.volume,
                          _chapter.number])),
        'pages': [request.build_absolute_uri(page.image.url)
                  for page in _chapter.pages.all()],
        'date': _chapter.date,
        'final': _chapter.final,
    }
    return JsonResponse(response) if json else response


def _volume_response(request, _series, vol, json=True):
    response = {}
    chapters = _series.chapters.filter(volume=vol)
    if chapters.count() == 0:
        return json_error('Not found', 404)
    for _chapter in chapters:
        response[_chapter.number] = _chapter_response(
            request, _chapter, json=False)
    return JsonResponse(response) if json else response


def _series_response(request, _series, json=True):
    response = {
        'title': _series.title,
        'aliases': [a.alias for a in _series.aliases.all()],
        'url': request.build_absolute_uri(
            reverse('reader:series', args={_series.slug})),
        'description': _series.description,
        'authors': [],
        'artists': [],
        'cover': request.build_absolute_uri(_series.cover.url),
        'volumes': {},
        'completed': _series.completed,
    }
    for _chapter in _series.chapters.all():
        if _chapter.volume not in response['volumes']:
            response['volumes'][_chapter.volume] = _volume_response(
                request, _series, _chapter.volume, json=False)
    for author in _series.authors.all():
        names = [author.name]
        for alias in author.aliases.all():
            names.append(alias.alias)
        response['authors'].append(names)
    for artist in _series.artists.all():
        names = [artist.name]
        for alias in artist.aliases.all():
            names.append(alias.alias)
        response['artists'].append(names)
    return JsonResponse(response) if json else response


@csrf_exempt
def all_releases(request):
    if request.method != 'GET':
        return json_error('Method not allowed', 405)
    _series = Series.objects.all()
    response = {}
    for s in _series:
        last_chapter = s.chapters.last()
        response[s.slug] = {
            'title': s.title,
            'url': request.build_absolute_uri(
                reverse('reader:series', args={s.slug})),
            'cover': request.build_absolute_uri(s.cover.url),
            'latest_chapter': {},
        }
        if last_chapter:
            response[s.slug]['latest_chapter'] = {
                'title': last_chapter.title,
                'volume': last_chapter.volume,
                'number': last_chapter.number,
                'date': last_chapter.date,
            }
    return JsonResponse(response)


@csrf_exempt
def all_series(request):
    if request.method != 'GET':
        return json_error('Method not allowed', 405)
    _series = Series.objects.all()
    response = {}
    for s in _series:
        response[s.slug] = _series_response(request, s)
    return JsonResponse(response)


@csrf_exempt
def series(request, slug=None):
    if request.method != 'GET':
        return json_error('Method not allowed', 405)
    try:
        _series = Series.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return json_error('Not found', 404)
    return _series_response(request, _series)


@csrf_exempt
def volume(request, slug=None, vol=0):
    if request.method != 'GET':
        return json_error('Method not allowed', 405)
    try:
        vol = int(vol)
        if vol < 0:
            raise ValueError
    except (ValueError, TypeError):
        return json_error('Bad request', 400)
    try:
        _series = Series.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return json_error('Not found', 404)
    return _volume_response(request, _series, vol)


@csrf_exempt
def chapter(request, slug=None, vol=0, num=0):
    if request.method != 'GET':
        return json_error('Method not allowed', 405)
    try:
        vol, num = int(vol), int(num)
        if vol < 0 or num < 0:
            raise ValueError
    except (ValueError, TypeError):
        return json_error('Bad request', 400)
    try:
        _chapter = Chapter.objects.get(series__slug=slug,
                                       volume=vol, number=num)
    except ObjectDoesNotExist:
        return json_error('Not found', 404)
    return _chapter_response(request, _chapter)


@csrf_exempt
def invalid_endpoint(request):
    return json_error('Invalid API endpoint', 501)

