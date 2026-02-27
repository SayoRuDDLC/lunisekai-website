from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, Http404
from .models import Anime, AnimeFormat, ReleaseSeason, Genre, AnimeStatus, Studio
from .forms import AddAnimeForm, TestForm


# Функции-хелперы
def get_anime_list(request, data, context=None, per_page=10):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get('page')  # Если параметр page отсутствует, то по умолчанию 1
    page_obj = paginator.get_page(page_number)

    if context is None:
        context = {}

    context['page_obj'] = page_obj

    template = (
        'anime/includes/anime_list_card.html'
        if request.headers.get('HX-Request')
        else 'anime/anime_list.html'
    )

    return render(request, template, context=context)


def ensure_not_empty(queryset):
    if not queryset.exists():
        raise Http404()
    return queryset


# Маршруты
def home(request):
    return render(request, 'anime/index.html')


def anime_detail(request, anime_slug):
    anime = get_object_or_404(
        Anime.objects.published().with_genres().with_episodes_count().with_episodes_numbers(),
        slug=anime_slug
    )

    return render(
        request, 'anime/anime_detail.html', context={'anime': anime}
    )


def anime_random(request):
    random_anime = Anime.objects.published().with_genres().with_episodes_count().random()

    if not random_anime:
        raise Http404()

    return redirect('anime:anime_detail', anime_slug=random_anime.slug)


def anime_list(request):
    data = Anime.objects.published().with_genres()

    if year_from := request.GET.get('year-from'):
        if year_from.isdigit() and int(year_from) > 0:
            data = data.filter(release_year__gte=year_from)
        else:
            year_from = ''
    if year_to := request.GET.get('year-to'):
        if year_to.isdigit():
            data = data.filter(release_year__lte=year_to)
        else:
            year_to = ''
    if genres := request.GET.getlist('genre'):
        data = data.filter(genres__slug__in=genres)
    if formats := request.GET.getlist('format'):
        data = data.filter(format__in=formats)
    if statuses := request.GET.getlist('status'):
        data = data.filter(status__in=statuses)
    if age_ratings := request.GET.getlist('age-rating'):
        data = data.filter(age_rating__in=age_ratings)

    selected_filters = {
        'selected_year_from': year_from,
        'selected_year_to': year_to,
        'selected_genres': genres,
        'selected_formats': formats,
        'selected_statuses': statuses,
        'selected_age_ratings': age_ratings,

    }

    context = {
        'list_title': 'Список аниме',
        **selected_filters,
    }

    return get_anime_list(request, data, context=context)


def anime_format(request, format_slug):
    data = ensure_not_empty(
        Anime.objects.published().with_genres().by_format(format=format_slug)
    )

    return get_anime_list(request, data, context={'list_title': f'Аниме по формату: {AnimeFormat(format_slug).label}'})


def anime_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    data = ensure_not_empty(
        Anime.objects.published().with_genres().by_genre(genre_slug=genre.slug)
    )

    return get_anime_list(request, data, context={'list_title': f'Аниме по жанру: {genre.name}'})


def anime_status(request, status_slug):
    data = ensure_not_empty(
        Anime.objects.published().with_genres().by_status(status=status_slug)
    )

    return get_anime_list(request, data, context={'list_title': f'Аниме по статусу: {AnimeStatus(status_slug).label}'})


def anime_studio(request, studio_slug):
    studio = get_object_or_404(Studio, slug=studio_slug)
    data = ensure_not_empty(
        Anime.objects.published().with_genres().by_studio(studio=studio.slug)
    )

    return get_anime_list(request, data, context={'list_title': f'Аниме студии: {studio.name}'})


def anime_season(request, season_slug=None, year=None):
    data = ensure_not_empty(
        Anime.objects.published().with_genres().by_season(season=season_slug, year=year)
    )

    season_label = ReleaseSeason(season_slug).label if season_slug else ""

    return get_anime_list(request, data, context={'list_title': f'Аниме по сезону: {season_label} {year or ""}'})


def add_anime(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # form.add_error('age_rating', 'В+хдфцзвхфцхвзцфв')
            print(form.cleaned_data)
    else:
        form = TestForm(initial={
            'title': 'Ыыы типа аниме'
        })

    return render(request, 'anime/add_anime.html', context={'form': form})


def manga_list(request):
    return render(request, 'anime/manga_list.html')


def novel_list(request):
    return render(request, 'anime/novel_list.html')
