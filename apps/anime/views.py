from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView, RedirectView, FormView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Anime, Genre, Studio
from .models import AnimeFormat, AnimeStatus, ReleaseSeason
from .utils import AnimeListMixin, AnimeFiltersMixin
from .forms import AddAnimeForm

'''
reverse() - используется в методах, когда код выполняется во время запроса
reverse_lazy() - используется в атрибутах класса, когда код выполняется при импорте
'''

class HomeView(TemplateView):
    template_name = 'anime/index.html'


class AnimeListView(AnimeListMixin, AnimeFiltersMixin, ListView):
    list_title = 'Список аниме'
    allow_empty = True

    def get_queryset(self):
        queryset = Anime.objects.published().with_genres()

        return self.get_filtered_queryset(queryset)


class AnimeFormatView(AnimeListMixin, ListView):
    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().by_format(format=self.kwargs['format_slug'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = f'Аниме по формату: {AnimeFormat(self.kwargs['format_slug']).label}'

        return context


class AnimeStatusView(AnimeListMixin, ListView):
    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().by_status(status=self.kwargs['status_slug'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = f'Аниме по статусу: {AnimeStatus(self.kwargs['status_slug']).label}'

        return context


class AnimeSeasonView(AnimeListMixin, ListView):
    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().by_season(
            season=self.kwargs.get('season'),
            year=self.kwargs.get('year')
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        season = self.kwargs.get('season') # Вернет объект ReleaseSeason или None
        season_label = season.label if season else ''
        year = self.kwargs.get('year') or ''

        context['list_title'] = f'Аниме по сезону: {season_label} {year}'

        return context



class AnimeGenreView(AnimeListMixin, ListView):
    def get_genre(self):
        if not hasattr(self, '_genre'):
            self._genre = get_object_or_404(Genre, slug=self.kwargs['genre_slug'])
        return self._genre

    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().by_genre(genre=self.get_genre().slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = f'Аниме по жанру: {self.get_genre().name}'

        return context


class AnimeStudioView(AnimeListMixin, ListView):
    def get_studio(self):
        if not hasattr(self, '_studio'):
            self._studio = get_object_or_404(Studio, slug=self.kwargs['studio_slug'])
        return self._studio

    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().by_studio(studio=self.get_studio().slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['list_title'] = f'Аниме студии: {self.get_studio().name}'

        return context


class AnimeDetailView(DetailView):
    template_name = 'anime/anime_detail.html'
    slug_url_kwarg = 'anime_slug'
    context_object_name = 'anime'

    def get_queryset(self):
        queryset = Anime.objects.published().with_genres().with_episodes()

        return queryset


class AnimeRandomView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        random_anime = Anime.objects.published().with_genres().with_episodes().random()

        if not random_anime:
            raise Http404

        return reverse('anime:anime_detail', kwargs={'anime_slug': random_anime.slug})


class AnimeEditorView(FormView):
    template_name = 'anime/add_anime.html'
    form_class = AddAnimeForm
    success_url = reverse_lazy('anime:add_anime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        anime_list = Anime.objects.order_updated()
        context['anime_list'] = anime_list

        return context

    # get_form_class должен возвращать всегда класс формы (AddAnimeForm), а не экземпляр (AddAnimeForm(...))
    # Для того, чтобы передавать в форму данные, нужно использовать get_form_kwargs
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        anime_id = self.request.POST.get('anime_id')
        if anime_id:
            anime = get_object_or_404(Anime, pk=anime_id)
            kwargs['instance'] = anime

        return kwargs


    def form_valid(self, form):
        form.save()
        message = 'Аниме успешно обновлено' if self.request.POST.get('anime_id') else 'Аниме успешно добавлено'
        messages.success(self.request, message)
        return super().form_valid(form)


class MangaListView(TemplateView):
    template_name = 'anime/manga_list.html'

class NovelListView(TemplateView):
    template_name = 'anime/novel_list.html'


# class MangaIndex(View):
#     def get(self, request):
#         return render(request, 'anime/manga_list.html', context={'title': 'МАНГА'})
#     def post(self, request):
#         pass
#
# class MangaIndex(TemplateView):
#     template_name = 'anime/manga_list.html'
#     # extra_context не позволяет передавать динамически получаемые данные (например из request.GET и т.д.)
#     # так как extra_context создает во время создания класса
#     # extra_context = {
#     #     'content': 'Это страница манги!'
#     # }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # context.update(self.extra_context) # добавляем в context наш extra_context
#         context['content'] = 'Это страница манги!'
#         return context

# class MangaIndex(ListView):
#     template_name = 'anime/manga_list.html'
#     context_object_name = 'manga_list'
#     extra_context = {
#         'title': 'Список манги'
#     }
#     allow_empty = False
#
#     def get_queryset(self):
#         # return Anime.objects.published().filter(slug=self.kwargs['slug'])
#         return Anime.objects.published()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#         # manga = context['manga_list'][0]
#

# class MangaIndex(DetailView):
#     template_name = 'anime/manga_list.html'
#     context_object_name = 'manga'
#     slug_url_kwarg = 'manga_slug'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Anime.objects.published(), slug=self.kwargs[self.slug_url_kwarg])

# class MangaIndex(FormView):
#     form_class = AddAnimeForm
#     template_name = 'anime/add_anime.html'
#     success_url = reverse_lazy('anime:home')
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['anime_form'] = context.pop('form') # удаляет form и возвращает его значение
#     #     return context
#
#     def form_valid(self, form):
#         form.save()
#         # return redirect('anime:home') # можно самому прописать redirect вместо return super().form_valid(form)
#         return super().form_valid(form) # вызывает стандартный redirect используя success_url

# class MangaIndex(CreateView):
#     form_class = AddAnimeForm
#     template_name = 'anime/add_anime.html'
#     success_url = reverse_lazy('anime:add_anime')

#     def get_success_url(self):
#         return reverse_lazy('profile', kwargs={'pk': self.object.pk})


# class MangaIndex(DataMixin, ListView):
#     template_name = 'anime/manga_list.html'
#     context_object_name = 'manga_list'
#     allow_empty = False
#     title_page = 'Страница мангиии'
#
#     def get_queryset(self):
#         return Anime.objects.published()

# class AnimeRandomView(RedirectView):
#     query_string = True
#     permanent = False
#     url = reverse_lazy('anime:anime_list')
#     pattern_name = 'anime:anime_list'