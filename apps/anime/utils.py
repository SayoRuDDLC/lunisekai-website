from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import AnimeFormat


# Миксины
class AnimeListMixin:
    list_title = None
    paginate_by = 10
    params_object_name = 'params'

    allow_empty = False

    template_name = 'anime/anime_list.html'
    htmx_template_name = 'anime/includes/anime_list_card.html'

    def get_template_names(self):
        if self.request.headers.get('HX-Request') and self.htmx_template_name:
            return [self.htmx_template_name] # Требуется вернуть список шаблонов
        return [self.template_name] # Возвращаем стандартный если не было HX-запроса или htmx_template_name = None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.list_title is not None:
            context['list_title'] = self.list_title

        params = self.request.GET.copy()
        params.pop('page', None)
        context[self.params_object_name] = params.urlencode()

        return context


class AnimeFiltersMixin:
    def get_filtered_queryset(self, queryset):
        if year_from := self.request.GET.get('year-from'):
            if year_from.isdigit() and int(year_from) > 0:
                queryset = queryset.filter(release_year__gte=year_from)
        if year_to := self.request.GET.get('year-to'):
            if year_to.isdigit():
                queryset = queryset.filter(release_year__lte=year_to)
        if genres := self.request.GET.getlist('genre'):
            queryset = queryset.filter(genres__slug__in=genres)
        if formats := self.request.GET.getlist('format'):
            queryset = queryset.filter(format__in=formats)
        if statuses := self.request.GET.getlist('status'):
            queryset = queryset.filter(status__in=statuses)
        if age_ratings := self.request.GET.getlist('age-rating'):
            queryset = queryset.filter(age_rating__in=age_ratings)

        return queryset

    def get_selected_filters(self):
        selected_filters = {
            'selected_year_from': self.request.GET.get('year-from'),
            'selected_year_to': self.request.GET.get('year-to'),
            'selected_genres': self.request.GET.getlist('genre'),
            'selected_formats': self.request.GET.getlist('format'),
            'selected_statuses': self.request.GET.getlist('status'),
            'selected_age_ratings': self.request.GET.getlist('age-rating'),
        }

        return selected_filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.get_selected_filters())

        return context