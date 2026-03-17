from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, Http404
from .models import Anime, Episode, EpisodeVideo
from functools import wraps
from django.utils.decorators import method_decorator
from .forms import AddAnimeForm


def htmx_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('HX-Request'):
            raise Http404()
        return view_func(request, *args, **kwargs)

    return wrapper


@htmx_only
def get_desc(request, anime_slug):
    full = request.GET.get('full') == 'true'
    anime = get_object_or_404(
        Anime.objects.published().only('desc'),
        slug=anime_slug,
    )
    template = 'anime/includes/anime_full_desc.html' if full else 'anime/includes/anime_short_desc.html'
    return render(request, template, {'anime': anime})



@htmx_only
def get_episode(request, anime_slug, episode_number):
    episode = get_object_or_404(Episode, anime__slug=anime_slug, number=episode_number)

    videos = episode.videos.all()
    voice_slug = request.GET.get('voice')

    if voice_slug:
        video = get_object_or_404(videos, voice__slug=voice_slug)
    else:
        video = videos.first()

    context = {
        'episode': episode,
        'videos': videos,
        'video': video,
        'active_voice_slug': voice_slug,
    }

    return render(request, 'anime/includes/anime_player.html', context=context)


@htmx_only
def edit_anime(request, anime_slug):
    anime = get_object_or_404(
        Anime.objects.select_related('studio').prefetch_related('genres'),
        slug=anime_slug
    )

    form = AddAnimeForm(instance=anime)
    return render(
        request, 'anime/includes/add_anime_form.html', context={'form': form, 'anime_id': anime.id}
    )

    # form = AddAnimeForm(
    #     initial={
    #         'title': anime.title,
    #         'release_year': anime.release_year,
    #         'release_season': anime.release_season,
    #         'format': anime.format,
    #         'age_rating': anime.age_rating,
    #         'publish_status': anime.publish_status,
    #         'title_alter': anime.title_alter,
    #         'slug': anime.slug,
    #         'desc': anime.desc,
    #         'genres': anime.genres.all(),
    #         'status': anime.status,
    #         'studio': anime.studio,
    #         'poster': anime.poster
    #     }
    # )


# from django.views.generic import UpdateView

# Через CBV
# @method_decorator(htmx_only, name="dispatch")
# class EditAnime(UpdateView):
#     model = Anime
#     form_class = AddAnimeForm
#     template_name = "anime/includes/add_anime_form.html"
#     slug_url_kwarg = "anime_slug"
#     slug_field = "slug"
#
#     def get_queryset(self):
#         return Anime.objects.select_related('studio').prefetch_related('genres')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["anime_id"] = self.object.id
#         return context